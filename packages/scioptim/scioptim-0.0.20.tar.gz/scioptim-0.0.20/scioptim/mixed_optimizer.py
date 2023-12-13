from __future__ import annotations
from typing import List, Type
import numpy as np
from scioptim import Optimizer, Model


class MixedOptimizer(Model, Optimizer):
    def __init__(self, optimizer: List[Type[Optimizer]], *args, **kwargs):
        self._optimizer = [opt(*args, **kwargs) for opt in optimizer]
        self._ismodel = [isinstance(opt, Model) for opt in self._optimizer]
        super().__init__(*args, **kwargs)
        if len(optimizer) < 1:
            raise ValueError(
                "At least one optimizer class must be passed (1 optimizer makes little sense,but ok)!"
            )

    def reset(self):
        for opt in self._optimizer:
            opt.reset()

    def sample(self, n) -> np.ndarray:
        ni = (
            np.ones(len(self._optimizer), dtype=int) * int(n / len(self._optimizer))
        ).astype(int)
        missing = n - ni.sum()
        ni[:missing] += 1

        dp = np.concatenate(
            [
                opt.sample(n, solve_categorical=False)
                for n, opt in zip(ni, self._optimizer)
            ],
            axis=0,
        )
        return dp

    @property
    def optimizer(self) -> List[Optimizer]:
        return self._optimizer

    @property
    def models(self) -> List[Model]:
        return [opt for i, opt in enumerate(self._optimizer) if self._ismodel[i]]

    def evaluate(self, x) -> np.ndarray:
        if not any(self._ismodel):
            raise NotImplementedError(
                "No model found in the optimizer, pass at least one optimizer with a model base class"
            )
        return np.stack(
            [opt.evaluate(x) for opt in self.models],
            axis=-1,
        )

    def fit(self, data: np.ndarray, append: bool = True) -> None:
        for i, opt in enumerate(self._optimizer):
            try:
                opt.fit(data, append=append)
            except NotImplementedError:
                pass
        return super().fit(data, append)

    def get_grid_points(
        self, evaluated: bool = True, grid_shape=True, **kwargs
    ) -> np.ndarray:
        opts = self.models
        sample_grid = opts[0].get_grid_points(
            evaluated=False, grid_shape=grid_shape, **kwargs
        )
        if not evaluated:
            return sample_grid

        if not grid_shape:
            g0 = sample_grid
        else:
            g0 = opts[0].get_grid_points(evaluated=False, grid_shape=False, **kwargs)

        g0 = np.concatenate([g0, self.evaluate(g0)], axis=-1)
        if grid_shape:
            g0 = g0.reshape(
                *sample_grid.shape[:-1], self.input_dim + self.output_dim * len(opts)
            )

        return g0

    def get_grid(self, steps=None, evaluated=True, input_ranges=None) -> np.ndarray:
        if not evaluated:
            return self.models[0].get_grid(
                steps=steps, evaluated=evaluated, input_ranges=input_ranges
            )

        return self.get_grid_points(
            steps=steps,
            evaluated=evaluated,
            input_ranges=input_ranges,
            grid_shape=True,
        )
