from .linear_regression import LinearRegression
from .helper_functions import get_variance, get_r_squared
import numpy as np
import numpy.typing as npt


class WLS(LinearRegression):

    def __init__(self):
        super().__init__()
        self._hat: npt.NDArray[np.float32] = 0
        self._annihilator = 0

    def fit(self, X: list[list[float]], Y: list[float], W: list[list[float]],
            intercept: bool = True) -> list[float]:

        if intercept is True:
            # add col for intercept
            X = np.column_stack((np.ones(X.shape[0]), X))

        b = np.atleast_2d(np.linalg.inv(X.T @ W @ X) @ X.T @ W @ Y)
        res = Y - (X @ b)

        n = len(X)
        p = len(X[0])

        # get sigma naive for r^2
        var = get_variance(n, p, res)

        self._betas = b
        self._residuals = res
        self._rsquared = get_r_squared(n, Y, var[0])
        self._sigma_naive = var[0]
        self._sigma_corrected = var[1]
        self._hat = X @ np.linalg.inv(X.T @ W @ X) @ X.T @ W
        self._annihilator = np.identity(X.shape[0]) - self._hat

        return b

    @property
    def hat(self):
        return self._hat

    @property
    def annihilator(self):
        return self._annihilator
