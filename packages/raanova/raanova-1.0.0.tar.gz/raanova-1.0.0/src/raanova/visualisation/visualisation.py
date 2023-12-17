import matplotlib.pyplot as plt
import numpy.typing as npt
import numpy as np


def display(X: npt.NDArray[np.float32],
            Y: npt.NDArray[np.float32],
            betas: npt.NDArray[np.float32] = None) -> None:

    if X.shape.count(1) != 1:
        raise ValueError("X must have exactly 1 dimension to be displayed")

    ax = plt.axes()
    ax.scatter(X, Y)

    a = np.array([X.min(), X.max()])

    if betas is not None:
        if len(betas) == 2:
            b = np.array([a[0]*betas[1], a[1]*betas[1]]) + betas[0]
        elif len(betas) == 1:
            b = np.array([a[0]*betas[0], a[1]*betas[0]])
        else:
            raise ValueError(
                "Betas may have at most 2 values (including intercept)")

        ax.plot(a, b, "r--")

    plt.show()
