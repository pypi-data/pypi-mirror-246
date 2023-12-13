from cf_units import Unit
import dask.array as da
import numpy as np

from ..dask_setup import progress
from .spell_kernels import make_first_spell_kernels, make_spell_length_kernels
from .support import (
    normalize_axis,
    IndexFunction,
    ThresholdMixin,
    ReducerMixin,
    DASK_OPERATORS,
)
from ..util import change_units


class FirstSpell(IndexFunction):
    def __init__(self, params):
        super().__init__(units=Unit("days"))
        self.params = params
        self.start_duration = self.params[0][2]
        if len(self.params) > 1:
            self.end_duration = self.params[1][2]
        else:
            self.end_duration = self.start_duration
        self.kernel = make_first_spell_kernels()

    def prepare(self, input_cubes):
        props = {
            (name, cube.dtype, cube.units, cube.standard_name)
            for name, cube in input_cubes.items()
        }
        for _, dtype, units, standard_name in props:
            for args in self.params:
                threshold = args[0]
                threshold.points = threshold.points.astype(dtype)
                if threshold.has_bounds():
                    threshold.bounds = threshold.bounds.astype(dtype)
                change_units(threshold, units, standard_name)
        super().prepare(input_cubes)

    def pre_aggregate_shape(self, *args, **kwargs):
        return (4,)

    def call_func(self, data, axis, **kwargs):
        raise NotImplementedError

    def lazy_func(self, data, axis, cube, client, **kwargs):
        axis = normalize_axis(axis, data.ndim)
        mask = da.ma.getmaskarray(data).any(axis=axis)
        data = da.moveaxis(data, axis, -1)
        length = data.shape[-1]
        time = da.arange(length, dtype=np.float32)
        output_dim = data.ndim
        output_shape = 6
        res_dim = output_dim + 1
        res_shape = 3  # start, end_independent, end_dependent
        data_idx = tuple(range(data.ndim))
        time_dim = data.ndim - 1
        time_idx = (time_dim,)
        output_idx = time_idx + data_idx[:-1] + (output_dim, res_dim)
        spell_res = da.blockwise(
            self.find_spell,
            output_idx,
            data,
            data_idx,
            time,
            time_idx,
            length=length,
            adjust_chunks={
                time_dim: lambda n: 1,
            },
            new_axes={
                output_dim: output_shape,
                res_dim: res_shape,
            },
            meta=np.array((), dtype=np.float32),
        )
        res = client.persist(
            da.reduction(
                spell_res,
                self.chunk,
                self.aggregate,
                combine=self.combine,
                axis=0,
                keepdims=True,
                concatenate=True,
                split_every=4,
                dtype=np.float32,
                meta=np.array((), dtype=np.float32),
            )
        )
        progress(res)
        res = res[0].copy()
        masked = da.ma.masked_array(
            da.ma.getdata(res),
            da.broadcast_to(mask[..., np.newaxis, np.newaxis], res.shape),
        )
        return masked[..., :2].astype(np.float32)

    def find_spell(self, chunk, time, length):
        def _first_spell(chunk_data, chunk_time, args):
            threshold, condition, duration, delay = args
            if length == 366 and delay == 182:
                delay += 1
            offset = np.where(delay <= chunk_time, True, False)
            thresholded_data = condition(chunk_data, threshold.points)
            thresholded_data = np.ma.filled(thresholded_data, fill_value=False)
            chunk_res = self.kernel.chunk(
                thresholded_data, offset, chunk_time, length, duration
            )
            return chunk_res

        no_end = np.full(chunk.shape[:-1] + (6,), fill_value=np.nan, dtype=np.float32)
        stack = []
        for args in self.params:
            chunk_res = _first_spell(chunk, time, args)
            stack.append(chunk_res)
        if len(self.params) == 1:
            stack.extend([no_end, no_end])
        else:
            end_dependent = stack[1].copy()
            start = stack[0][..., 2]
            cond = da.greater_equal(start, end_dependent[..., 2])
            for ind in np.ndindex(chunk.shape[:-1]):
                if cond[ind]:
                    start_offset = int(time[0]) + start[ind] + 1
                    end_params = self.params[1][:-1] + (start_offset,)
                    chunk_res = _first_spell(chunk[ind], time, end_params)
                    end_dependent[ind] = chunk_res
            stack.append(end_dependent)
        res = da.stack(stack, axis=-1)
        return res.reshape((1,) + res.shape)

    def chunk(self, x_chunk, axis, keepdims, computing_meta=False):
        if computing_meta:
            return np.array((), dtype=np.float32)
        return x_chunk

    def combine(self, x_chunk, axis, keepdims):
        res = self.kernel.combine(
            np.array(x_chunk), self.start_duration, self.end_duration
        )
        return res.reshape((1,) + res.shape)

    def aggregate(self, x_chunk, axis, keepdims):
        res = self.kernel.combine(
            np.array(x_chunk), self.start_duration, self.end_duration
        )
        res = self.kernel.aggregate(res)
        return res.reshape((1,) + res.shape)

    def post_process(self, cube, chunk_data, coords, period, **kwargs):
        def _get_ind(ind, axis):
            length = ind + (0, axis)
            index = ind + (2, axis)
            head = ind + (4, axis)
            tail = ind + (5, axis)
            return length, index, head, tail

        def _fuse(this, next_chunk):
            res = this.copy()
            for ind in np.ndindex(this.shape[:2]):
                ind_length, ind_start_index, _, ind_start_tail = _get_ind(ind, axis=0)
                _, ind_end_index, _, ind_end_tail = _get_ind(ind, axis=1)
                _, _, ind_next_start_head, _ = _get_ind(ind, axis=0)
                _, _, ind_next_end_head, _ = _get_ind(ind, axis=1)
                if da.isnan(this[ind_start_index]):
                    start_spell = this[ind_start_tail] + next_chunk[ind_next_start_head]
                    if start_spell >= self.start_duration:
                        res[ind_start_index] = (
                            this[ind_length] - this[ind_start_tail] + 1
                        )
                        end_tail = this[ind_end_tail]
                        if this[ind_end_tail] >= this[ind_start_tail]:
                            end_tail = this[ind_start_tail] - 1
                        end_spell = end_tail + next_chunk[ind_next_end_head]
                        if not da.isnan(end_spell):
                            if end_spell >= self.end_duration:
                                res[ind_end_index] = this[ind_length] - end_tail + 1
                            elif res[ind_start_index] == this[ind_length]:
                                res[ind_end_index] = np.nan
                            else:
                                res[ind_end_index] = this[ind_length]
                else:
                    if da.isnan(this[ind_end_index]):
                        end_spell = this[ind_end_tail] + next_chunk[ind_next_end_head]
                        if not da.isnan(end_spell):
                            if end_spell >= self.end_duration:
                                res[ind_end_index] = (
                                    this[ind_length] - this[ind_end_tail] + 1
                                )
                            else:
                                res[ind_end_index] = this[ind_length]
            return res

        mask = da.ma.getmaskarray(chunk_data)
        stack = []
        this = da.ma.getdata(chunk_data[0])
        tmp_res = da.empty(this.shape, dtype=np.float32)
        padding_chunk = da.zeros((1,) + this.shape, dtype=np.float32)
        padded_data = da.concatenate([da.ma.getdata(chunk_data), padding_chunk], axis=0)
        for next_chunk in padded_data[1:]:
            tmp_res = da.blockwise(
                _fuse,
                (0, 1, 2, 3),
                this,
                (0, 1, 2, 3),
                next_chunk,
                (0, 1, 2, 3),
                meta=np.array((), dtype=np.float32),
            )
            stack.append(tmp_res)
            this = next_chunk
        res_chunk = da.stack(stack, axis=0)
        masked_res = da.ma.masked_array(res_chunk, mask)
        return masked_res


class SeasonStart(FirstSpell):
    def __init__(self, **params):
        args = [
            (
                params["threshold"],
                DASK_OPERATORS[params["condition"]],
                params["duration"].points[0],
                params["delay"].points[0],
            )
        ]
        super().__init__(args)

    def lazy_func(self, data, axis, **kwargs):
        res = super().lazy_func(data, axis, **kwargs)
        return res

    def post_process(self, cube, data, coords, period, **kwargs):
        res = super().post_process(cube, data, coords, period, **kwargs)
        start = res[..., 0]
        return cube, start[..., 2].astype(np.float32)


class SeasonEnd(FirstSpell):
    def __init__(self, **params):
        args = [
            (
                params["start_threshold"],
                DASK_OPERATORS[params["start_condition"]],
                params["start_duration"].points[0],
                params["start_delay"].points[0],
            ),
            (
                params["end_threshold"],
                DASK_OPERATORS[params["end_condition"]],
                params["end_duration"].points[0],
                params["end_delay"].points[0],
            ),
        ]
        super().__init__(args)

    def lazy_func(self, data, axis, **kwargs):
        res = super().lazy_func(data, axis, **kwargs)
        return res

    def post_process(self, cube, data, coords, period, **kwargs):
        res = super().post_process(cube, data, coords, period, **kwargs)
        end = res[..., 1]
        return cube, end[..., 2].astype(np.float32)


class SeasonLength(FirstSpell):
    def __init__(self, **params):
        args = [
            (
                params["start_threshold"],
                DASK_OPERATORS[params["start_condition"]],
                params["start_duration"].points[0],
                params["start_delay"].points[0],
            ),
            (
                params["end_threshold"],
                DASK_OPERATORS[params["end_condition"]],
                params["end_duration"].points[0],
                params["end_delay"].points[0],
            ),
        ]
        super().__init__(args)

    def lazy_func(self, data, axis, **kwargs):
        res = super().lazy_func(data, axis, **kwargs)
        return res

    def post_process(self, cube, data, coords, period, **kwargs):
        res = super().post_process(cube, data, coords, period, **kwargs)
        start = res[..., 0]
        end = res[..., 1]
        length = end[..., 2] - start[..., 2] + 1
        length = da.ma.where(np.isnan(length), 0, length)
        return cube, length.astype(np.float32)


class SpellLength(ThresholdMixin, ReducerMixin, IndexFunction):
    def __init__(self, threshold, condition, statistic, fuse_periods=False):
        super().__init__(threshold, condition, statistic, units=Unit("days"))
        self.spanning_spells = True
        self.kernels = make_spell_length_kernels(self.scalar_reducer)
        self.fuse_periods = fuse_periods

    def pre_aggregate_shape(self, *args, **kwargs):
        return (4,)

    def call_func(self, data, axis, **kwargs):
        axis = normalize_axis(axis, data.ndim)
        mask = np.ma.getmaskarray(data).any(axis=axis)
        res = np.apply_along_axis(self, axis=axis, arr=data)
        res = np.ma.masked_array(np.ma.getdata(res), mask)
        return res.astype("float32")

    def lazy_func(self, data, axis, **kwargs):
        axis = normalize_axis(axis, data.ndim)
        mask = da.ma.getmaskarray(data).any(axis=axis)
        data = da.moveaxis(data, axis, -1)
        res = da.reduction(
            data,
            self.chunk,
            self.aggregate,
            keepdims=True,
            output_size=4,
            axis=-1,
            dtype=int,
            concatenate=False,
            meta=np.array((), dtype=int),
        )
        res = da.ma.masked_array(
            da.ma.getdata(res), np.broadcast_to(mask[..., np.newaxis], res.shape)
        )
        return res.astype("float32")

    def chunk(self, raw_data, axis, keepdims, computing_meta=False):
        if computing_meta:
            return np.array((), dtype=int)

        data = self.condition(raw_data, self.threshold.points)
        data = np.ma.filled(data, fill_value=False)
        chunk_res = self.kernels.chunk(data)
        return chunk_res

    def aggregate(self, x_chunk, axis, keepdims):
        if not isinstance(x_chunk, list):
            return x_chunk
        res = self.kernels.aggregate(np.array(x_chunk))
        return res

    def post_process(self, cube, data, coords, period, **kwargs):
        def fuse(this, previous_tail):
            own_mask = da.ma.getmaskarray(this[..., 0])
            own_length = this[..., 0]
            own_head = this[..., 1]
            internal = this[..., 2]
            own_tail = this[..., 3]
            head = da.where(own_head, previous_tail + own_head, 0.0)
            tail = da.where(own_length == own_head, previous_tail + own_tail, own_tail)
            stack = da.stack([head, internal, tail], axis=-1)
            spell_length = da.ma.masked_array(
                self.lazy_reducer(stack, axis=-1), own_mask
            )
            return spell_length, tail

        if self.fuse_periods and len(data) > 1:
            stack = []
            this = data[0]
            slice_shape = this.shape[:-1]
            previous_tail = da.ma.masked_array(
                da.zeros(slice_shape, dtype=np.float32),
                da.ma.getmaskarray(data[0, ..., 3]),
            )

            for next_chunk in data[1:]:
                spell_length, previous_tail = fuse(this, previous_tail)
                stack.append(spell_length)
                this = next_chunk

            stack.append(fuse(next_chunk, previous_tail)[0])
            res_data = da.stack(stack, axis=0)
        else:
            res_data = self.lazy_reducer(data[..., 1:], axis=-1)
        return cube, res_data
