from .linear_regression import LinearRegression
import numpy as np
import numpy.typing as npt
from .helper_functions import (
    get_variance, get_r_squared, get_OLS_AIC_BIC, get_OLS_CI
    )


class OLS(LinearRegression):
    def __init__(self):
        super().__init__()
        self._conf_interval: npt.NDArray[np.float32] = 0
        self._AIC = 0
        self._BIC = 0
        self._hat: npt.NDArray[np.float32] = 0
        self._annihilator = 0

    def fit(self,
            X: npt.NDArray[np.float32], Y: npt.NDArray[np.float32],
            intercept: bool = True, alpha: float = 0.05
            ) -> npt.NDArray[np.float32]:

        if intercept is True:
            # add col for intercept
            X = np.column_stack((np.ones(X.shape[0]), X))

        self._using_ols = True
        # Calculate the coefficients using the normal equation
        b = np.atleast_2d(np.linalg.inv(X.T @ X) @ X.T @ Y)
        self._betas = b

        res = Y - (X @ b)

        n = len(X)
        p = len(X[0])
        var = get_variance(n, p, res)

        self._residuals = res
        self._rsquared = get_r_squared(n, Y, var[0])
        self._sigma_naive = var[0]
        self._sigma_corrected = var[1]
        self._hat = X @ np.linalg.inv(X.T @ X) @ X.T
        self._annihilator = np.identity(X.shape[0]) - self._hat

        aic_bic = get_OLS_AIC_BIC(Y, X @ b, n, p)
        self._conf_interval = get_OLS_CI(
            b, self._sigma_corrected, X, n, p, alpha)
        self._AIC = aic_bic[0]
        self._BIC = aic_bic[1]

        return self._betas

    @property
    def AIC(self):
        return self._AIC

    @property
    def BIC(self):
        return self._BIC

    @property
    def hat(self):
        return self._hat

    @property
    def annihilator(self):
        return self._annihilator

    @property
    def conf_interval(self):
        return self._conf_interval
