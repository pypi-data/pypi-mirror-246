import unittest
from raanova.linear_regression.ols import OLS
import numpy as np


class TestOLS(unittest.TestCase):
    def test_base(self):
        X = np.random.uniform(-1, 1, (100, 5))
        e = np.random.normal(0, 0.1, (100, 1))
        Y = (0.5 + 1.0*X[:, 0] + 1.0*X[:, 1]+1.0*X[:, 2]).reshape(-1, 1)+e

        ols = OLS()
        ols.fit(X, Y)

        print(f"betas:\n{ols._betas}")
        print(f"res: {ols._residuals[:10, :]}")
        print(f"r_sqrd: {ols._rsquared}")
        print(f"naive: {ols._sigma_naive}")
        print(f"corrected: {ols._sigma_corrected}")
        print(f"conf_int:\n{ols._conf_interval}")
        print(f"aic:\n{ols._AIC}")
        print(f"bic:\n{ols._BIC}")

        ols.summary()
