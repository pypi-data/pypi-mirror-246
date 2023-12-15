"""File with iterations re-weigthed regression model algorithm."""
# Third Party Library
import numpy as np

from pamm.algorithms.regression.regression_model import RegressionAlgorithm


class IterationsReWeightedRegressionAlgorithm(RegressionAlgorithm):
    def fit(
        self,
        x: np.ndarray,
        y: np.ndarray,
        weights_function: any,
        max_iter: int = 10
        ) -> None:
        """Fit model.

        Args:
            x (np.ndarray): matrix of regressors
            y (np.ndarray): matrix a teacher
            weights_function (any): algorithm for calculate weights
            max_iter (int): count iterations for reweighted data
        """

        x = self._add_bias(x)
        tmp = np.linalg.inv(x.T @ w @ x) @ x.T @ w @ y
        self._beta = tmp[int(self._fit_bias) :]
        self._bias = tmp[0][0] * int(self._fit_bias)