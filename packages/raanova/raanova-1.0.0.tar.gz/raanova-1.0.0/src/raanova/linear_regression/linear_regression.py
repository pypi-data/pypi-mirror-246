import numpy as np
import numpy.typing as npt
from .helper_functions import CI_pretty_print


class LinearRegression:
    def __init__(self):
        self._residuals: npt.NDArray[np.float32] = 0
        self._rsquared: float = 0
        self._betas: npt.NDArray[np.float32] = 0
        self._sigma_naive: float = 0
        self._sigma_corrected: float = 0
        self._using_ols: bool = False
        self._conf_interval: npt.NDArray[np.float32] = 0
        self._AIC = 0
        self._BIC = 0
        self._hat: npt.NDArray[np.float32] = 0
        self._annihilator = 0

    def fit(
       self, X: npt.NDArray[np.float32], Y: npt.NDArray[np.float32]
       ) -> npt.NDArray[np.float32]:
        pass

    def predict(self, X: npt.NDArray[np.float32], intercept: bool = True
                ) -> npt.NDArray[np.float32]:
        if intercept:
            X = np.column_stack((np.ones(X.shape[0]), X))
        return X @ self._betas

    def summary(self) -> None:
        # residuals section:
        # min/max/med/quartiles
        min_res = round(np.min(self._residuals), 5)
        Q1 = round(np.percentile(self._residuals, 25), 5)
        median = round(np.percentile(self._residuals, 50), 5)
        Q3 = round(np.percentile(self._residuals, 75), 5)
        max_res = round(np.max(self._residuals), 5)

        beta_i = []
        for i in range(0, len(self._betas)):
            beta_i.append('beta_' + str(i))

        print(
            f"{'Residuals:': <10}\n"
            f"{'Min': <10}{'Q1': ^10}{'Med': ^10}{'Q3': ^10}{'Max': >5}"
            f"\n{min_res: <10}{Q1: ^10}{median: ^10}{Q3: ^10}{max_res: >5}")
        print("\n")
        print('Coefficients      Estimates')

        for a, b in zip(beta_i, self._betas):
            print(f"{a: <10}        {round(b[0], 5): <10}")
        print()

        if self._using_ols is True:
            CI_pretty_print(self._conf_interval, len(self._betas))

        print(
            '\n\nR-squared: ' + str(round(self._rsquared, 5))
            + '\nNaive estimator: ' + str(round(self._sigma_naive, 5))
            + '\nCorrected naive estimator: '
            + str(round(self._sigma_corrected, 5)))

        if self._using_ols is True:
            print(
                '\nAIC: ' + str(round(self._AIC, 5))
                + '\nBIC: ' + str(round(self._BIC, 5)))

    @property
    def residuals(self):
        return self._residuals

    @property
    def rsquared(self):
        return self._rsquared

    @property
    def sigma_naive(self):
        return self._sigma_naive

    @property
    def sigma_corrected(self):
        return self._sigma_corrected

    @property
    def betas(self):
        return self._betas
