from collections import namedtuple

import numpy as np
from numba import jit

Kernels = namedtuple(
    "Kernels", ["chunk", "aggregate", "combine", "post_process"], defaults=[None, None]
)


def make_first_spell_kernels():
    # The gufunc support in numba is lacking right now.
    # Once numba supports NEP-20 style signatures for
    # gufunc, we can use @guvectorize to vectorize this
    # function, allowing for more general applicability
    # in terms of dimensions and hopefully better performance,
    # perhaps taking advantage of GPUs. The template is
    # @guvectorize([float32, int64], '(n)->(4)')
    # def chunk_column(column, res):
    @jit(nopython=True)
    def chunk_column(column, minimum_length):
        """Calculate first spell information for a single timeseries.

        Parameters
        ----------
        column : np.array
            1d array containing the timeseries

        Returns
        -------
        np.array
            4 vector containing the first spell information, namely:
            - length of timeseries
            - length of spell at beginning
            - position of first spell in the timeseries
            - length of spell at the end
        """
        res = np.empty((4,), dtype=np.float32)
        n = column.shape[0]
        where = np.flatnonzero
        x = column[1:] != column[:-1]
        starts = where(x) + 1
        no_runs = len(starts)
        # the length of the chunk is n
        res[0] = n
        # assume no internal spell
        res[2] = np.nan
        # if no change occurs, then...
        if no_runs == 0:
            # ...either the spell covers the entire chunk, or...
            if column[0]:
                res[1] = n
                if n >= minimum_length:
                    res[2] = 0
                res[3] = n
            # ...there is no spell in this chunk
            else:
                res[1] = 0
                res[3] = 0
        else:
            # there is a spell from the beginning to the first change
            # if the first value is part of a spell
            res[1] = starts[0] if column[0] else 0
            # there is a spell from the last change to the end if
            # the last value is part of a spell
            res[3] = n - starts[-1] if column[starts[-1]] else 0
            # if there is a sufficiently long spell at the beginning, we're done
            if res[1] >= minimum_length:
                res[2] = 0
                return res
            # if there is a sufficiently long spell at the end,
            # we don't need to look at more chunks in the aggregation
            if res[3] >= minimum_length:
                res[2] = starts[-1]
            # if there are at least two changes (range(1) = [0])
            for k in range(no_runs - 1):
                # if the value at the corresponding change is part
                # of a spell then this spell stretches to the next
                # change and is an internal spell
                if column[starts[k]]:
                    length = starts[k + 1] - starts[k]
                    if length >= minimum_length:
                        res[2] = starts[k]
                        return res
        return res

    @jit(nopython=True)
    def find_edge_spell(thresholded_data, cond, i, minimum_length):
        offset_data = np.logical_and(cond, thresholded_data)
        spell_lengths = np.argwhere(offset_data == 0)
        if len(spell_lengths) > 0:
            if i == 0:
                res = spell_lengths[0][0]
            else:
                res = offset_data.shape[-1] - spell_lengths[-1][0] - 1
        else:
            if thresholded_data.shape[-1] > minimum_length:
                res = minimum_length - 1
            else:
                res = thresholded_data.shape[-1]
        return res

    @jit(nopython=True)
    def chunk(thresholded_data, offset, chunk_time, length, minimum_length):
        res = np.empty(thresholded_data.shape[:-1] + (6,), dtype=np.float32)
        start_spell = np.where(chunk_time < (minimum_length - 1), True, False)
        end_spell = np.where(chunk_time > (length - minimum_length), True, False)
        for ind in np.ndindex(*thresholded_data.shape[:-1]):
            offset_data = np.logical_and(offset, thresholded_data[ind])
            res[ind][:-2] = chunk_column(offset_data, minimum_length)
            for i, cond in enumerate([start_spell, end_spell]):
                if cond.any():
                    res[ind][-(2 - i)] = find_edge_spell(
                        thresholded_data[ind], cond, i, minimum_length
                    )
                else:
                    res[ind][-(2 - i)] = 0
        return res

    @jit(nopython=True)
    def combine(x_chunk, start_duration, end_duration):
        def _merge_chunks(chunks, this, minimum_length):
            this = this.copy()
            # mark where this chunk is completely covered by a spell
            this_full = np.asarray(this[..., 0] == this[..., 1])
            for k in range(1, chunks.shape[0]):
                next_chunk = chunks[k]
                for ind in np.ndindex(this.shape[:-1]):
                    ind_length = ind + (0,)
                    ind_head = ind + (1,)
                    ind_internal = ind + (2,)
                    ind_tail = ind + (3,)
                    ind_spell_start = ind + (4,)
                    ind_spell_end = ind + (5,)
                    # if the start edge spell covers the chunk
                    start_full = np.asarray(this[ind_spell_start] == this[ind_length])
                    if start_full:
                        this[ind_spell_start] += next_chunk[ind_spell_start]
                    # if the end edge spell covers the next chunk
                    end_full = np.asarray(
                        next_chunk[ind_spell_end] == next_chunk[ind_length]
                    )
                    if end_full:
                        this[ind_spell_end] += next_chunk[ind_spell_end]
                    else:
                        this[ind_spell_end] = next_chunk[ind_spell_end]
                    # the next chunk is completely covered by a spell
                    next_full = next_chunk[ind_length] == next_chunk[ind_head]
                    # if both are completely covered the merged chunk
                    # is completely covered too
                    if this_full[ind] and next_full:
                        this[ind_head] += next_chunk[ind_head]
                        this[ind_tail] += next_chunk[ind_tail]
                        if this[ind_head] >= minimum_length:
                            this[ind_internal] = 0
                    # if the old chunk is completely covered, but the new one
                    # isn't, then
                    elif this_full[ind]:
                        # the head is the old head + the new head,
                        this[ind_head] += next_chunk[ind_head]
                        # the internal spell is the new internal spell,
                        if this[ind_head] >= minimum_length:
                            this[ind_internal] = 0
                        else:
                            this[ind_internal] = (
                                this[ind_length] + next_chunk[ind_internal]
                            )
                        # the tail is the new tail,
                        this[ind_tail] = next_chunk[ind_tail]
                        # and the resulting chunk is no longer fully covered
                        this_full[ind] = False
                    # if the old chunk is not fully covered, but the new one is
                    elif next_full:
                        old_tail = this[ind_tail]
                        # the tail is the old tail + the new head
                        this[ind_tail] += next_chunk[ind_head]
                        if this[ind_tail] >= minimum_length and np.isnan(
                            this[ind_internal]
                        ):
                            this[ind_internal] = this[ind_length] - old_tail
                    # if neither are fully covered
                    else:
                        # the head stays the same,
                        # the internal spell is the winner between
                        # the old internal spell, the new internal spell,
                        # and the internal spell resulting from merging
                        # old tail and new head,
                        if np.isnan(this[ind_internal]):
                            length = this[ind_tail] + next_chunk[ind_head]
                            if length >= minimum_length:
                                this[ind_internal] = this[ind_length] - this[ind_tail]
                            elif not np.isnan(next_chunk[ind_internal]):
                                this[ind_internal] = (
                                    this[ind_length] + next_chunk[ind_internal]
                                )
                        # and the tail is the new tail
                        this[ind_tail] = next_chunk[ind_tail]
                    # the length of the combined chunks is the sum of the
                    # lengths of the individual chunks
                    this[ind_length] += next_chunk[ind_length]
            return this

        def _find_overlap(chunks, this, ind, minimum_length):
            this = this.copy()
            length = chunks[0][ind][0, 0]
            for k in range(1, chunks.shape[0]):
                current = chunks[k - 1][ind]
                next_chunk = chunks[k][ind]
                ind_length = (0, 0)
                ind_internal_start = (2, 0)
                ind_internal_end = (2, 1)
                ind_internal_end_dep = (2, 2)
                ind_head_end = (1, 1)
                ind_tail_start = (3, 0)
                ind_tail_end = (3, 1)
                start_ind = this[ind_internal_start]
                # if there is not a dependent end after the start
                if length >= start_ind and not this[ind_internal_end_dep] > start_ind:
                    # if there is a dependent end after the start
                    if current[ind_internal_end_dep] > start_ind:
                        this[ind_internal_end_dep] = current[ind_internal_end_dep]
                    # if there is a end between the chunks
                    elif (
                        current[ind_tail_end] + next_chunk[ind_head_end]
                        >= minimum_length
                    ):
                        new_tail = current[ind_tail_start] - 1
                        # if the end is after the start
                        if length - current[ind_tail_end] > start_ind:
                            this[ind_internal_end_dep] = length - current[ind_tail_end]
                        # if there is a valid end after the start
                        elif new_tail + next_chunk[ind_head_end] >= minimum_length:
                            this[ind_internal_end_dep] = length - new_tail
                        else:
                            # if there is a independent end in the next chunk
                            if length + next_chunk[ind_internal_end] > start_ind:
                                this[ind_internal_end_dep] = (
                                    length + next_chunk[ind_internal_end]
                                )
                    # the end might be in the next chunk
                    else:
                        # there is an independent end
                        if length + next_chunk[ind_internal_end] > start_ind:
                            this[ind_internal_end_dep] = (
                                length + next_chunk[ind_internal_end]
                            )
                # if the start is in the next chunk
                elif (
                    length + next_chunk[ind_length] >= start_ind
                    and not this[ind_internal_end_dep] > start_ind
                ):
                    # if there is a independent end after the start
                    if length + next_chunk[ind_internal_end] > start_ind:
                        this[ind_internal_end_dep] = (
                            length + next_chunk[ind_internal_end]
                        )
                    # if there is a dependent end after the start
                    elif length + next_chunk[ind_internal_end_dep] > start_ind:
                        this[ind_internal_end_dep] = (
                            length + next_chunk[ind_internal_end_dep]
                        )
                length += next_chunk[ind_length]
            # if there is no end found after the start
            if this[ind_internal_end_dep] <= start_ind:
                this[ind_internal_end_dep] = np.nan
            return this

        # if there is only one chunk
        res = x_chunk[0].copy()
        # if there are more than one chunk
        if x_chunk.shape[0] > 1:
            # find start
            res[..., 0] = _merge_chunks(x_chunk[..., 0], res[..., 0], start_duration)
            # if we have conditions for finding an end
            if not np.isnan(res[..., 0, 1]).any():
                # find end independent of start
                res[..., 1] = _merge_chunks(x_chunk[..., 1], res[..., 1], end_duration)
                # if the end index is before of at the same time as the start index
                # update the dependent end
                for ind in np.ndindex(res.shape[:-2]):
                    ind_start = ind + (2, 0)
                    ind_end = ind + (2, 1)
                    if res[ind_start] >= res[ind_end]:
                        res[ind] = _find_overlap(x_chunk, res[ind], ind, end_duration)
        return res

    @jit(nopython=True)
    def aggregate(res):
        for ind in np.ndindex(res.shape[:-2]):
            ind_start = ind + (2, 0)
            ind_end = ind + (2, 1)
            ind_end_dep = ind + (2, 2)
            # if there is no start there is no end
            if np.isnan(res[ind_start]):
                res[ind_end] = np.nan
            # if the independent end is before or at the same time as the start
            # set the end to the dependent end
            elif res[ind_start] >= res[ind_end]:
                res[ind_end] = res[ind_end_dep]
            res[ind_start] += 1
            res[ind_end] += 1
        return res

    return Kernels(chunk, aggregate, combine)


def make_spell_length_kernels(reducer):
    # The gufunc support in numba is lacking right now.
    # Once numba supports NEP-20 style signatures for
    # gufunc, we can use @guvectorize to vectorize this
    # function, allowing for more general applicability
    # in terms of dimensions and hopefully better performance,
    # perhaps taking advantage of GPUs. The template is
    # @guvectorize([float32, int64], '(n)->(4)')
    # def chunk_column(column, res):
    @jit(nopython=True)
    def chunk_column(column):
        res = np.empty((4,), dtype=np.int64)
        n = column.shape[0]
        where = np.flatnonzero
        x = column[1:] != column[:-1]
        starts = where(x) + 1
        no_runs = len(starts)
        # the length of the chunk is n
        res[0] = n
        # assume no internal spell
        res[2] = 0
        # if no change occurs, then...
        if no_runs == 0:
            # ...either the spell covers the entire chunk, or...
            if column[0]:
                res[1] = n
                res[3] = n
            # ...there is no spell in this chunk
            else:
                res[1] = 0
                res[3] = 0
        else:
            # there is a spell from the beginning to the first change
            # if the first value is part of a spell
            res[1] = starts[0] if column[0] else 0
            # there is a spell from the last change to the end if
            # the last value is part of a spell
            res[3] = n - starts[-1] if column[starts[-1]] else 0
            # if there are at least two changes (range(1) = [0])
            for k in range(no_runs - 1):
                # if the value at the corresponding change is part
                # of a spell then this spell stretches to the next
                # change and is an internal spell
                if column[starts[k]]:
                    length = starts[k + 1] - starts[k]
                    res[2] = reducer(length, res[2])
        return res

    @jit(nopython=True)
    def chunk(thresholded_data):
        res = np.empty(thresholded_data.shape[:-1] + (4,), dtype=np.int64)
        for ind in np.ndindex(*thresholded_data.shape[:-1]):
            res[ind] = chunk_column(thresholded_data[ind])
        return res

    @jit(nopython=True)
    def aggregate(x_chunk):
        # start with the first chunk and merge all others subsequently
        res = x_chunk[0].copy()
        # mark where this chunk is completely covered by a spell
        this_full = np.asarray(res[..., 0] == res[..., 1])
        for k in range(1, x_chunk.shape[0]):
            next_chunk = x_chunk[k]
            for ind in np.ndindex(res.shape[:-1]):
                ind_length = ind + (0,)
                ind_head = ind + (1,)
                ind_internal = ind + (2,)
                ind_tail = ind + (3,)
                # the next chunk is completely covered by a spell
                next_full = next_chunk[ind_length] == next_chunk[ind_head]
                # the length of the combined chunks is the sum of the
                # lengths of the individual chunks
                res[ind_length] += next_chunk[ind_length]
                # if both are completely covered the merged chunk
                # is completely covered too
                if this_full[ind] and next_full:
                    res[ind_head] += next_chunk[ind_head]
                    res[ind_tail] += next_chunk[ind_tail]
                # if the old chunk is completely covered, but the new one
                # isn't, then
                elif this_full[ind]:
                    # the head is the old head + the new head,
                    res[ind_head] += next_chunk[ind_head]
                    # the internal spell is the new internal spell,
                    res[ind_internal] = next_chunk[ind_internal]
                    # the tail is the new tail,
                    res[ind_tail] = next_chunk[ind_tail]
                    # and the resulting chunk is no longer fully covered
                    this_full[ind] = False
                # if the old chunk is not fully covered, but the new one is
                elif next_full:
                    # the tail is the old tail + the new head
                    res[ind_tail] += next_chunk[ind_head]
                # if neither are fully covered
                else:
                    # the head stays the same,
                    # the internal spell is the winner between
                    # the old internal spell, the new internal spell,
                    # and the internal spell resulting from merging
                    # old tail and new head,
                    res[ind_internal] = reducer(
                        res[ind_internal],
                        res[ind_tail] + next_chunk[ind_head],
                        next_chunk[ind_internal],
                    )
                    # and the tail is the new tail
                    res[ind_tail] = next_chunk[ind_tail]
        return res

    return Kernels(chunk, aggregate)
