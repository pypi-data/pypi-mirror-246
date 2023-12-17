import unittest
from raanova.linear_regression.wls import WLS
import numpy as np


class TestWLS(unittest.TestCase):
    def test_1(self):
        X = np.random.uniform(-1, 1, (100, 5))
        e = np.random.normal(0, 0.1, (100, 1))
        Y = (0.5 + 1.0*X[:, 0] + 1.0*X[:, 1]+1.0*X[:, 2]).reshape(-1, 1)+e

        wls = WLS()
        W = np.diag(np.full(len(X), 1))
        wls.fit(X, Y, W)

        wls.summary()
