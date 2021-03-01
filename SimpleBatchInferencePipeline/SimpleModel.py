import numpy as np
from sklearn.base import RegressorMixin

# A simple model that returns the length of the input
class SimpleModel(RegressorMixin):
    def __init__(self, feature_name):
        self.feature_name = feature_name

    def fit(self, X=None, y=None):
        print("Nothing to do with the data")
        return self

    def predict(self, X=None):
        return X[self.feature_name].astype(str).map(len)
