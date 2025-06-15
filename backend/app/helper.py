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

