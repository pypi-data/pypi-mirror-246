import numpy as np
import pandas as pd
from sklearn.linear_model import HuberRegressor
from sklearn.metrics import r2_score


def _shift_data(X, y, n):
    # +ve: features predict previous value, -ve: features predict next value
    if n == 0:
        return X, y
    return (X[n:], y[:-n]) if n > 0 else (X[:n], y[-n:])


def _add_lagged_y_to_x(X, y, n):
    # TODO add lagged response to feature, n is (list of) lag
    pass


class LinearRegressor(object):
    def __init__(self, fitter=HuberRegressor(), transform=None, invtransform=None):
        """Basic linear regression model

        Args:
            fitter (scikit-learn model, optional): Model object with fit(), predict() and score(). Defaults to HuberRegressor().
            transform (Function, optional): Transformation applied to data, e.g. log. Defaults to None.
            invtransform (Function, optional): Function to invert transform, e.g. exp. Defaults to None.
        """
        self.fitter = fitter
        identity = (lambda x: x)
        self.transform = identity if transform is None else transform
        self.invtransform = identity if invtransform is None else invtransform
        self.prediction = None
        self.observed = None
        self.R2 = 0
        self.shift = 0

    def fit(self, X, y, shift=0, **kwargs):
        """Fit linear model to data

        Args:
            X (array): features
            y (array): response
            shift (int, optional): shift in y. Positive means current features are used to predict previous response. 
            Negative means current features are used to predict next response. Defaults to 0.
        """
        self.shift = shift
        X, y = _shift_data(X, y, shift)
        self.observed = y
        X_transformed = self.transform(X)
        y_transformed = self.transform(y)
        self.fitter.fit(X_transformed, y_transformed, **kwargs)
        self.ypred = self.invtransform(self.fitter.predict(X_transformed))
        self.R2 = r2_score(y, self.ypred)

    def rolling_fit(self, X, y, shift=0, window=1, **kwargs):
        """Run a rolling fit prediction over the dataset

        Args:
            X (array): features
            y (array): response
            shift (int, optional): shift in y. Positive means current features are used to predict previous response. 
            Negative means current features are used to predict next response. Defaults to 0.
            window (int, optional): Size of the rolling window. Defaults to 1.
        """
        self.shift = shift
        X, y = _shift_data(X, y, shift)
        self.observed = y
        X_transformed = np.asarray(self.transform(X))
        y_transformed = np.asarray(self.transform(y))

        # loop over windows
        ypred = []
        R2 = []
        coeffs = []
        for start_ind in range(len(y)-window):
            Xw = X_transformed[start_ind:start_ind+window]
            yw = y_transformed[start_ind:start_ind+window]
            self.fitter.fit(Xw, yw, **kwargs)
            ypred.append(self.invtransform(self.fitter.predict(X_transformed)))
            R2.append(r2_score(y, self.ypred))
            coeffs.append(self.fitter.coef_)

        return pd.concat([pd.DataFrame(ypred, columns=['Prediction']), pd.DataFrame(R2, columns=['R2']), pd.DataFrame(coeffs)], axis=1)

    def predict(self, X, **kwargs):
        """Predict on feature.

        Args:
            X (array): features

        Returns:
            prediction (array): predicted response
        """
        self.prediction = self.invtransform(
            self.fitter.predict(self.transform(X), **kwargs))
        return self.prediction
