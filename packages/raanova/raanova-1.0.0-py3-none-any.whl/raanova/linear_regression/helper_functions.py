import numpy as np
import numpy.typing as npt

from scipy.stats import t


def MSE(Y_true, Y_pred):
    return (1 / Y_true.shape[0]) * np.linalg.norm(Y_true - Y_pred)**2


def get_residuals(
    X: npt.NDArray[np.float32],
    Y: npt.NDArray[np.float32],
    betas: npt.NDArray[np.float32]
        ) -> npt.NDArray[np.float32]:
    return Y - (X @ betas)


def get_variance(
        n: float, p: float, residuals: npt.NDArray[np.float32]
        ) -> list[float]:
    sigma_naive = (1 / n) * np.linalg.norm(residuals)**2
    sigma_corrected = (n / (n - p)) * sigma_naive

    return [sigma_naive, sigma_corrected]


def get_r_squared(
        n: float, Y: npt.NDArray[np.float32], sigma_naive: float
        ) -> float:
    y_mean = (1 / n) * np.sum(Y)
    y_mean_vectorize = np.full((n, 1), y_mean)

    return 1 - (n * sigma_naive) / (np.linalg.norm(y_mean_vectorize)**2)


def get_OLS_hat_ann_matrix(
        X: npt.NDArray[np.float32]
        ) -> list[npt.NDArray[np.float32]]:
    hat_mtx = X @ np.linalg.inv(X.T @ X) @ X.T
    return [hat_mtx, np.identity(X.shape[0]) - hat_mtx]


def get_ridge_hat_ann_matrix(
        X: npt.NDArray[np.float32],
        penalty: np.float32,
        ) -> list[npt.NDArray[np.float32]]:
    hat_mtx = \
        X @ np.linalg.inv(X.T @ X + penalty*np.identity(X.shape[1])) @ X.T
    return [hat_mtx, np.identity(X.shape[0]) - hat_mtx]


def get_OLS_CI(
        betas: npt.NDArray[np.float32],
        sigma_corr: float,
        X: npt.NDArray[np.float32],
        n: int,
        p: int,
        alpha: float = 0.05
        ) -> list[npt.NDArray[np.float32]]:

    t_alpha = t.ppf(1 - alpha / 2, n - p)

    range = np.full((p, 1), t_alpha) \
        * np.sqrt(sigma_corr) \
        * np.linalg.inv(np.diagonal(X.T @ X) * np.identity(p))**0.5
    range = np.diag(range).reshape(-1, 1)

    return [betas - range, betas + range]


def get_OLS_AIC_BIC(
    Y_true: npt.NDArray[np.float32],
    Y_pred: npt.NDArray[np.float32],
    n: int,
    p: int
        ) -> list[float, float]:
    return [
        -n * np.log(MSE(Y_true, Y_pred)) + 2 * p,
        -n * np.log(MSE(Y_true, Y_pred)) + p * np.log(n)
        ]


def CI_pretty_print(CI, num_beta):
    print("Coefficients      Confidence Interval")
    for j in range(num_beta):
        lower_j = round(CI[0][j, 0], 5)
        upper_j = round(CI[1][j, 0], 5)
        print(f"beta_{j}            [{lower_j}; {upper_j}]")
