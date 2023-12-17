import numpy as np

from .linear_regression import LinearRegression
from .helper_functions import get_residuals, get_variance, get_r_squared


class Lasso(LinearRegression):
    def __init__(self):
        super().__init__()
        self._penalty = 0

    def fit(
            self,
            X: list[list[float]],
            Y: list[float],
            intercept: bool = True,
            penalty: float = 0.1,
            step_size: float = 0.01,
            max_iter: int = 1000
            ) -> list[float]:
        self._penalty = penalty
        self._step_size = step_size

        if intercept:
            X = np.column_stack((np.ones(X.shape[0]), X))

        n, p = X.shape

        # initialize parameters
        self._betas = np.random.rand(p, 1)

        # run coordinate descent
        for _ in range(max_iter):
            # compute subgradient descent at each coordinate
            for i in range(p):
                # compute subgradient
                if self._betas[i, :] > 0:
                    d_beta_i = (-2 / n) * (
                        (X[:, i] @ (Y - X@self._betas)) + self._penalty)
                else:
                    # we take subgradient at beta_j = 0 to be -1 since
                    # sugradient at 0 in [-1, 1]
                    d_beta_i = (-2 / n) * (
                        (X[:, i] @ (Y - X@self._betas)) - self._penalty)

                # compute subgradient descent at coordinate i
                self._betas[i, :] -= self._step_size * d_beta_i

        # establish other statistics
        self._residuals = get_residuals(X, Y, self._betas)
        self._sigma_naive, self._sigma_corrected = get_variance(
            n, p, self._residuals)
        self._rsquared = get_r_squared(n, Y, self._sigma_naive)

        return self._betas
