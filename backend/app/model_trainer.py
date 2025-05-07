from pathlib import Path
from typing import Union, Optional

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score
import joblib

pd.set_option("future.no_silent_downcasting", True)


class DataPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.num_imputer = SimpleImputer(strategy="median")
        self.cat_imputer = SimpleImputer(strategy="most_frequent")
        self.categorical_features = None
        self.numeric_features = None
        self.fill_values_ = None

    def fit(self, X, y=None):
        """Обучает компоненты предобработки данных:

        1. Предобработку колонки с количеством мест
        2. Удаление неиспользуемых колонок колонок
        3. Заполнение пропущенных значений особым способом
        4. Определение числовых и категориальных признаков
        5. Обучение импутеров для разных типов признаков

        Возвращает:
            self (ModelTrainer): Обученный объект трансформера
        """
        _ = y  # чтобы убрать предупреждение
        df = X.copy()
        df = self._process_seats(df)
        df = self._remove_columns(df)

        self.fill_values_ = {
            "fuel_rate": df["fuel_rate"].median(),
            "pts_original": True,
            "accidents_resolution": "OK",
            "auto_class": "NOT SPECIFIED",
        }

        self._custom_imputation(df)

        self.numeric_features = df.select_dtypes(include="number").columns.tolist()
        self.categorical_features = df.select_dtypes(include=["object", "category"]).columns.tolist()

        self.num_imputer.fit(df[self.numeric_features])
        self.cat_imputer.fit(df[self.categorical_features])

        return self

    def transform(self, X):
        """Применяет обученные преобразования к входным данным:
        1. Обработку колонки с количеством мест
        2. Удаление лишних колонок
        3. Заполнение пропущенных значений особым способом
        4. Применение обученных импутеров
        5. Приведение типов данных

        Возвращает:
            pd.DataFrame: Обработанные данные после всех преобразований
        """
        df = X.copy()
        df = self._process_seats(df)
        df = self._remove_columns(df)
        df = self._custom_imputation(df)

        if self.numeric_features:
            df[self.numeric_features] = self.num_imputer.transform(df[self.numeric_features])
        if self.categorical_features:
            df[self.categorical_features] = self.cat_imputer.transform(df[self.categorical_features])

        return self._cast_types(df)

    def _remove_columns(self, df):
        return df.drop(
            columns=[
                "tags",
                "complectation_available_options",
                "equipment",
                "horse_power",
                "seats",
            ],
            errors="ignore",
        )

    def _process_seats(self, df):
        if "seats" not in df.columns:
            print("Столбец 'seats' отсутствует!")

        df["seats_numeric"] = df["seats"].apply(self._convert_seats)
        return df

    def _custom_imputation(self, df):
        df.fillna(value=self.fill_values_, inplace=True)
        return df

    def _cast_types(self, df):
        for col in self.numeric_features:
            df[col] = df[col].astype("float32")
        for col in self.categorical_features:
            df[col] = df[col].astype("category")
        return df

    @staticmethod
    def _convert_seats(seats: Optional[Union[int, str, float]]) -> Union[int, float]:
        """
        Конвертирует значение seats в максимальное целое число из списка
        или возвращает np.nan при ошибке.

        """
        try:
            if seats is None or (isinstance(seats, float) and np.isnan(seats)):
                return np.nan

            if isinstance(seats, str):
                if ";" in seats:
                    return max(map(int, seats.split(";")))
                return int(seats)

            return int(float(seats))

        except (ValueError, TypeError):
            return np.nan


class ModelTrainer:
    def __init__(self):
        self.pipeline = None

    def build_pipeline(self, numeric_features, categorical_features):
        """Создаем весь пайплайн из:
        -DataPreprocessor()
        -StandardScaler() для числовых признаков
        -OneHotEncoder() для категориальных признаков
        """
        numeric_transformer = Pipeline(steps=[("scaler", StandardScaler())])

        categorical_transformer = Pipeline(steps=[("onehot", OneHotEncoder(handle_unknown="ignore"))])

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", numeric_transformer, numeric_features),
                ("cat", categorical_transformer, categorical_features),
            ]
        )

        self.pipeline = Pipeline(
            steps=[
                ("cleaner", DataPreprocessor()),
                ("preprocessor", preprocessor),
                ("regressor", Ridge(alpha=1, solver="auto")),
            ]
        )

    def train(self, data: pd.DataFrame, params: dict):
        """Обучает модель на предоставленных данных с использованием заданных параметров.

        возвращает:
            метрики и пайплайн.
        """
        try:
            data.dropna(subset=["price"], inplace=True)

            X = data.drop(columns=["price"])
            y = data["price"]

            temp_df = DataPreprocessor().fit_transform(X)
            numeric_features = temp_df.select_dtypes(include=["number"]).columns.tolist()
            categorical_features = temp_df.select_dtypes(include=["category"]).columns.tolist()

            self.build_pipeline(numeric_features, categorical_features)

            self.pipeline.set_params(
                regressor__alpha=params.get("alpha", 1.0),
                regressor__max_iter=params.get("max_iter", 100),
                regressor__solver=params.get("solver", "auto"),
            )

            print("Начато обучение модели")
            self.pipeline.fit(X, y)

            return {"metrics": self._calculate_metrics(X, y), "pipeline": self.pipeline}
        except Exception as e:
            print("Ошибка обучения модели :", str(e))
            raise

    def _calculate_metrics(self, X, y):
        y_pred = self.pipeline.predict(X)
        return {
            "r2_score": r2_score(y, y_pred),
            "rmse": np.sqrt(mean_squared_error(y, y_pred)),
        }

    def save_model(self, model_path: str):
        """Сохраняет обученный пайплайн модели в файл.
        Создает нужные директории при отсутствии.
        """
        Path(model_path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.pipeline, model_path)
