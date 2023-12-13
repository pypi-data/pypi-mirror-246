import numpy as np
from typing import Literal
from scioptim import Optimizer


class BaseGridSearch(Optimizer):
    """
    A base class for grid search optimization, extending from the Optimizer class.

    This class provides a basic framework for sampling points from a predefined grid of sample points.
    It is designed to be extended by specific grid search implementations.

    Methods:
        sample(n: int) -> np.ndarray: Samples a specified number of points from the grid.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the BaseGridSearch optimizer.
        """
        self._grid_sample_points: np.ndarray = None
        super().__init__(*args, **kwargs)

    def sample(self, n: int):
        """
        Samples a specified number of points from the predefined grid.

        Args:
            n (int): The number of points to sample.

        Returns:
            np.ndarray: An array of sampled points.

        Raises:
            ValueError: If 'n' is greater than the number of available grid points.
        """
        if n > self._grid_sample_points.shape[0]:
            raise ValueError(
                f"n must be smaller or equal to the number of available grid points ({self._grid_sample_points.shape[0]})"
            )

        out = self._grid_sample_points[:n]
        self._grid_sample_points = self._grid_sample_points[n:]
        return out

    def map_points_to_resolution(self, points: np.ndarray, unique=False) -> np.ndarray:
        """
        Grid search optimizers should not map points to resolution, so this method returns the points unchanged.
        """

        # make points unique
        if unique:
            points = np.unique(points, axis=0)
        return points


class GridSearch(BaseGridSearch):
    """
    A grid search optimizer for systematic sampling across a multidimensional grid.

    This class extends BaseGridSearch and allows for the creation of a grid with specified resolution in each dimension. The grid can be randomized or kept in a fixed order.

    Attributes:
        _res (Union[int, np.ndarray]): The resolution of the grid in each dimension.
        _randomize (bool): Whether to randomize the order of the grid points.

    Methods:
        __init__(res: Union[int, np.ndarray], randomize: bool, *args, **kwargs): Initializes the GridSearch optimizer.
        reset(): Resets and initializes the grid based on the current settings.
    """

    def __init__(self, randomize=True, *args, **kwargs):
        """
        Initializes the GridSearch optimizer with specified resolution and optional randomization.

        Args:
            res (Union[int, np.ndarray]): The resolution of the grid. If an integer is provided, it is used for all dimensions.
            randomize (bool, optional): Determines whether the grid points should be randomized. Defaults to True.
            *args: Variable-length argument list for the base class.
            **kwargs: Arbitrary keyword arguments for the base class.
        """
        self._randomize = randomize

        super().__init__(*args, **kwargs)

    def reset(self):
        """
        Resets and initializes the grid based on the current resolution and range settings.
        """

        grids = self._resolution_grids
        if any([g is None for g in grids]):
            raise ValueError(
                "Grid resolution must be specified, either by provifing input_steps or input_resolution"
            )

        self._grid_sample_points = np.meshgrid(
            *[self._resolution_grids[i] for i in range(self.input_dim)]
        )
        self._grid_sample_points = np.hstack(
            [s.flatten()[:, None] for s in self._grid_sample_points]
        )

        self._grid_sample_points = np.unique(self._grid_sample_points, axis=0)

        if self._randomize:
            self.rnd_gen.shuffle(self._grid_sample_points)


class CentralCompositeDesign(BaseGridSearch):
    """
    A Central Composite Design (CCD) optimizer for experimental design, typically used in response surface methodology.

    This class extends BaseGridSearch and creates a CCD grid which can be circumscribed, inscribed, or faced. The design can be rotatable or orthogonal.

    Attributes:
        _type (str): The type of CCD ('circumscribed', 'inscribed', or 'faced').
        _design (str): The design type ('rotatable' or 'orthogonal').

    Methods:
        __init__(n: int, type: str, design: str, *args, **kwargs): Initializes the CentralCompositeDesign optimizer.
        reset(): Resets and initializes the CCD grid based on the current settings.
    """

    def __init__(
        self,
        type: Literal["circumscribed", "inscribed", "faced"] = "circumscribed",
        design: Literal["rotatable", "orthogonal"] = "rotatable",
        randomize=True,
        *args,
        **kwargs,
    ):
        """
        Initializes the CentralCompositeDesign optimizer with the specified number of points, type, and design.

        Args:
            n (int): The number of factorial points.
            type (str, optional): The type of CCD ('circumscribed', 'inscribed', or 'faced'). Defaults to 'circumscribed'.
            design (str, optional): The design type ('rotatable' or 'orthogonal'). Defaults to 'rotatable'.
            *args: Variable-length argument list for the base class.
            **kwargs: Arbitrary keyword arguments for the base class.

        Raises:
            AssertionError: If the 'type' or 'design' arguments are invalid.
        """

        self._randomize = randomize
        if type not in ["circumscribed", "inscribed", "faced"]:
            raise ValueError(
                f"type must be one of 'circumscribed','inscribed','faced' ({type} given)"
            )

        if design not in ["rotatable", "orthogonal"]:
            raise ValueError(
                f"design must be one of 'rotatable','orthogonal' ({design} given)"
            )
        self._type = type
        self._design = design
        super().__init__(*args, **kwargs)

    def reset(self):
        """
        Resets and initializes the Central Composite Design grid based on the current settings, type, and design.
        """
        steps = self.input_sizes
        for i, s in enumerate(steps[1:]):
            if s != steps[0]:
                raise ValueError("CCD requires equal step sizes in all dimensions")
        n = steps[0]
        if n is None:
            raise ValueError("CCD requires step sizes to be specified")
        if n < 2:
            raise ValueError("CCD requires at least 2 points in each dimension")

        _F = np.meshgrid(*[np.linspace(-1, 1, n) for i in range(self.input_dim)])
        _F = np.hstack([s.flatten()[:, None] for s in _F])
        _C = np.zeros((1, self.input_dim))

        _N0 = 1
        _Nf = 2**self.input_dim
        _N = 2**self.input_dim + 2 * self.input_dim + _N0
        _T = 2 * self.input_dim + _N0
        _div = 1
        if self._design == "rotatable":
            _alpha = np.power(_Nf, 1 / 4)
            if self._type == "circumscribed":
                _div = _alpha
            elif self._type == "inscribed":
                _alpha = 1 / _alpha
            elif self._type == "faced":
                _alpha = 1

        elif self._design == "orthogonal":
            _alpha = np.power(
                ((np.sqrt(_Nf + _T) - np.sqrt(_Nf)) ** 2) * _Nf / 4, 1 / 4
            )
            _div = _alpha
            if self._type == "circumscribed":
                _div = _alpha**2
            elif self._type == "inscribed":
                _alpha = 1 / _alpha
            elif self._type == "faced":
                _alpha = 1

        if self.input_dim > 1:
            _E = np.zeros((self.input_dim, self.input_dim))
        else:
            _E = np.zeros((0, self.input_dim))

        np.fill_diagonal(_E, _alpha)
        _E = np.vstack([_E, -_E])

        self._grid_sample_points = np.concatenate([_F, _C, _E], axis=0)
        self._grid_sample_points = self._grid_sample_points + 1 * _div
        self._grid_sample_points = self._grid_sample_points / (2 * _div)

        self._grid_sample_points = (
            self._grid_sample_points
            * (self.input_ranges[:, 1] - self.input_ranges[:, 0])
            + self.input_ranges[:, 0]
        )

        self._grid_sample_points = np.unique(self._grid_sample_points, axis=0)
        if self._randomize:
            self.rnd_gen.shuffle(self._grid_sample_points)
