from typing import Callable, List, Protocol
import numpy as np
from scipy.optimize import fmin
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, VotingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt
import tqdm


class LossFunction(Protocol):
    def loss(self, y_true, y_pred) -> float:
        raise NotImplementedError("loss function is not implemented")

    def grad(self, y_true, y_pred):
        raise NotImplementedError("gradient function is not implemented")


class SquareLoss:
    def loss(self, y_true, y_pred) -> float:
        return ((y_true - y_pred) ** 2).sum()

    def grad(self, y_true, y_pred):
        return 2 * (y_pred - y_true)


def get_initialization_constant(y_true, loss: LossFunction) -> float:
    def _total_loss(gamma):
        gammas = gamma * np.ones_like(y_true)
        return loss.loss(y_true, gammas)

    g_opt, *_ = fmin(_total_loss, 1.0, disp=0, full_output=1)
    return g_opt[0]


def get_multiplier(y_true, old_pred, new_pred, loss: LossFunction) -> float:
    def _total_loss(gamma):
        return loss.loss(y_true, old_pred + gamma * new_pred)

    g_opt, *_ = fmin(_total_loss, 1.0, disp=0, full_output=1)
    return g_opt[0]


class GBDT:
    def __init__(self, loss, regressor_factory, iterations, learning_rate):
        self.gammas = []
        self.regressors = []
        self.loss: LossFunction = loss
        self.iterations = iterations
        self.learning_rate = learning_rate
        self.regressor_factory = regressor_factory

    def fit(self, X, y):
        self.init_constant = get_initialization_constant(y, self.loss)
        preds = self.init_constant * np.ones_like(y)
        for _ in tqdm.trange(self.iterations):
            pseudo_residuals = self.loss.grad(y, preds)
            regressor = self.regressor_factory()
            regressor.fit(X, pseudo_residuals)
            self.regressors.append(regressor)
            new_preds = regressor.predict(X)
            gamma = self.learning_rate * get_multiplier(y, preds, new_preds, self.loss)
            self.gammas.append(gamma)
            preds += gamma * new_preds

    def predict(self, X):
        out = self.init_constant
        for gamma, regressor in zip(self.gammas, self.regressors):
            out += gamma * regressor.predict(X)
        return out


from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split

from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Perceptron
from sklearn.compose import TransformedTargetRegressor

regressor_factory = lambda: TransformedTargetRegressor(
    regressor=DecisionTreeRegressor(max_depth=2),
    func=lambda x: x,
    inverse_func=lambda x: x,
    check_inverse=False,
)


data: dict = load_diabetes()  # type: ignore
X = data["data"]
y = data["target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

gbdt = GBDT(
    loss=SquareLoss(),
    regressor_factory=regressor_factory,
    iterations=1000,
    learning_rate=0.01,
)
gbdt.fit(X_train, y_train)
y_pred = gbdt.predict(X_test)
p = np.poly1d(np.polyfit(y_test, y_pred, 1))
plt.scatter(y_test, y_pred)
plt.plot(
    [y_test.min(), y_test.max()],
    [p(y_test.min()), p(y_test.max())],
    "r--",
    lw=2,
)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "k--", lw=2)
plt.show()
