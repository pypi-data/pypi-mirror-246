# Imports
import numpy as np
from raanova import OLS
from raanova.visualisation import display

# Generate the dataset to perform regression on
# the true model is y = 0*1 + 1*x0 + 2*x1 + 4*x2
X = np.random.rand(200, 1) * 100
true_beta = np.atleast_2d([2]).T
epsilon = np.random.randn(200, 1)
Y = X @ true_beta + epsilon

# Fit
model = OLS()
beta_hat = model.fit(X, Y, intercept=False, alpha=0.05)

# Display model information
model.summary()

# Make predictions on new data
X_test = np.random.rand(10, 1) * 100
y_hat = model.predict(X_test, intercept=False)
print(y_hat)

display(X, Y, beta_hat)
