import os
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000")
TIMEOUT = 10


def get_models():
    """
    Получить список доступных моделей с бэкенда.

    Делает GET-запрос к {API_URL}/models и возвращает JSON-массив:
    [
      {"id": "...", "name": "...", "params": {...}, "metrics": {...}},
      ...
    ]
    """
    resp = requests.get(f"{API_URL}/models", timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def set_model(model_id: int):
    """
    POST /models/{model_id}/set

    Установить активную модель по её ID.

    Args:
        model_id: Идентификатор модели для установки активной.

    Returns:
        Ответ сервера с подтверждением:
        {
            "status": str,
            "active_model": int
        }
    """
    resp = requests.post(f"{API_URL}/models/{model_id}/set", timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def fit_model_json(df_records: list, params: dict):
    """
    Запустить обучение на JSON-данных.

    Args:
        records: Список объектов (list of dict), каждый — одна строка датасета.
        params: Словарь гиперпараметров.

    Returns:
        Ответ бэкенда с model_id, статусом и т.д.
    """
    payload = {"data": df_records, "params": params, "xml_params": ""}
    resp = requests.post(f"{API_URL}/fit/json", json=payload, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def fit_model_csv(df, params: dict, xml_params: str = ""):
    """
    POST /fit/csv

    Обучение модели на данных в формате CSV.

    Args:
        df: pandas.DataFrame с данными.
        params: Параметры обучения (query-параметры).
        xml_params: Параметры в формате XML (необязательно).

    Returns:
        Ответ сервера с метаданными обучения.
    """
    query = {k: v for k, v in params.items() if v is not None}
    files = {"file": ("data.csv", df.to_csv(index=False).encode("utf-8"), "text/csv")}
    data = {"params_json": ""}
    data.update({})
    resp = requests.post(
        f"{API_URL}/fit/csv",
        params=query,
        data={"xml_params": xml_params},
        files=files,
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()


def predict_json(features: dict):
    """
    POST /predict/json

    Предсказание цены на основе одного или нескольких объектов в формате JSON.

    Args:
        features: dict с признаками автомобиля.

    Returns:
        Список предсказанных цен (list of float).
    """
    payload = [features]
    resp = requests.post(f"{API_URL}/predict/json", json=payload, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def predict_csv(df):
    """
    POST /predict/csv

    Предсказание цен для пакета данных в формате CSV.

    Args:
        df: pandas.DataFrame с признаками автомобилей.

    Returns:
        Список предсказанных цен (list of float).
    """
    files = {"file": ("data.csv", df.to_csv(index=False).encode("utf-8"), "text/csv")}
    resp = requests.post(f"{API_URL}/predict/csv", files=files, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()
