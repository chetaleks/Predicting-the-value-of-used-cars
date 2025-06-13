from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class MissingValueImputer(BaseEstimator, TransformerMixin):
    """
    Импутирует пропуски: медианой для числовых и модой для категориальных.
    feature_types: dict, ключи — имена признаков, значения — 'numeric' или 'categorical'
    """
    def __init__(self, feature_types):
        self.feature_types = feature_types

    def fit(self, X, y=None):
        X = X.copy()
        self.impute_values_ = {}
        for col, typ in self.feature_types.items():
            if col in X.columns:
                if typ == 'numeric':
                    num = pd.to_numeric(X[col], errors='coerce')
                    self.impute_values_[col] = num.median()
                else:
                    mode_vals = X[col].mode(dropna=True)
                    self.impute_values_[col] = mode_vals.iloc[0] if not mode_vals.empty else 0
        return self

    def transform(self, X):
        X = X.copy()
        X['pts_original'] = X['pts_original'].fillna(True)
        X['accidents_resolution'] = X['accidents_resolution'].fillna('OK')
        for col, val in self.impute_values_.items():
            if col in X.columns:
                if self.feature_types.get(col) == 'numeric':
                    X[col] = pd.to_numeric(X[col], errors='coerce').fillna(val)
                else:
                    X[col] = X[col].fillna(val)
        return X
       