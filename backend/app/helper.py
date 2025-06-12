from pathlib import Path

from fastapi import HTTPException
from pydantic import ValidationError
import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from scipy.cluster import hierarchy
from scipy.spatial.distance import squareform
from pandas.api.types import is_numeric_dtype

from .schemas import CarFeatures


def check_csv_file(file) -> pd.DataFrame:
    """Проверка входного файла csv"""

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(400, "Разрешена загрузка только .csv файлов")
    try:
        df = pd.read_csv(file.file)

        for _, row in df.iterrows():
            CarFeatures(**row.dropna().to_dict())

        return df
    except (ValidationError, pd.errors.ParserError) as e:
        raise HTTPException(422, str(e)) from e


def get_active_model_path(shared_state: dict) -> str:
    """Возвращает путь к активной модели"""

    if not shared_state.get("active_model_id"):
        raise HTTPException(400, detail="Активная модель не выбрана")

    model_id = shared_state["active_model_id"]
    model_info = shared_state["models"].get(model_id)

    if not model_info:
        raise HTTPException(404, detail="Модель не найдена")

    model_path = model_info.get("model_path")

    if not model_path or not Path(model_path).exists():
        raise HTTPException(500, detail="Файл модели не найден")

    return model_path


def prepare_new_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавляет новые признаки для моделей CatBoost и LightGBM.
    Преобразования взяты из feature_engineering.ipynb:
      - age = current_year - production_year
      - km_per_year = mileage / age
      - power_to_rate = engine_power / fuel_rate
      - log_mileage = log1p(mileage)
      - condition_score: mapping категорий condition -> числовая шкала
      - is_high_mileage = mileage > 200000
      - disp_category: бинам по engine_displacement
    """
    df = df.copy()

    df['age'] = 2025 - df['production_year']
    df['km_per_year'] = df['mileage'] / df['age'].replace(0, 1)
    df['power_to_rate'] = df['engine_power'] / df['fuel_rate'].replace(0, 1)
    df['log_mileage'] = np.log1p(df['mileage'])

    condition_map = {
        'new': 5, 'like new': 4, 'excellent': 4,
        'good': 3, 'fair': 2, 'poor': 1
    }
    df['condition_score'] = df['condition'].map(condition_map).fillna(3)

    df['is_high_mileage'] = (df['mileage'] > 200000).astype(int)

    bins = [0, 1.0, 2.0, 3.0, 5.0, np.inf]
    labels = ['very_small', 'small', 'medium', 'large', 'very_large']
    df['disp_category'] = pd.cut(df['engine_displacement'], bins=bins, labels=labels)

    cat_cols = [
        'region', 'seller_type', 'brand', 'model',
        'body_type', 'steering_wheel', 'price_segment',
        'auto_class', 'tags', 'equipment', 'complectation_available_options'
    ]
    for col in cat_cols:
        df[col] = df[col].fillna('unknown')

    return df


