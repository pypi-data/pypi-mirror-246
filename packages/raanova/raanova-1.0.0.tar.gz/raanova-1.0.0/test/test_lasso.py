import unittest
from src.raanova.linear_regression.lasso import Lasso
import numpy as np


class TestLasso(unittest.TestCase):
    def test_base(self):
        X = np.random.uniform(-1, 1, (100, 5))
        e = np.random.normal(0, 0.1, (100, 1))
        Y = (0.5 + 1.0*X[:, 0] + 1.0*X[:, 1] + 1.0*X[:, 2]).reshape(-1, 1) + e

        m1 = Lasso()
        m1.fit(X, Y)
        print(f"betas:\n{m1._betas}")
        print(f"residuals: {m1._residuals[:10, :]}")
        print(f"r_squared: {m1._rsquared}")
        print(f"sigma_naive: {m1._sigma_naive}")
        print(f"sigma_corr: {m1._sigma_corrected}")
