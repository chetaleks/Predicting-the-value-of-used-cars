import json
import sys
import uuid
import traceback
from contextlib import asynccontextmanager
from multiprocessing import Manager
from pathlib import Path
from typing import List, Optional
from xml.parsers.expat import ExpatError

import joblib
import pandas as pd
import xmltodict
from fastapi import Body, FastAPI, File, HTTPException, Form, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from sklearn.linear_model import Ridge

from .helper import check_csv_file, get_active_model_path, prepare_new_features
from .schemas import (
    CarFeatures,
    HyperParams,
    ModelInfo,
    FitRequestJson,
    FitRequestQueryParams,
)
from .train_process import _start_training
from .paths import MODELS_DIR

from . import (
    model_trainer as _mt,
)  # Чтобы установить инициализированную модель


sys.modules["model_trainer"] = _mt  # Чтобы установить инициализированную модель

pd.set_option("future.no_silent_downcasting", True)

shared_state = {
    "models": {},           # обычный словарь
    "active_model_id": None
}

STANDARD_MODELS = {
    "final_model",
    "catboost_pipeline",
    "catboost_pipeline_old",
    "lgbm_pipeline",
    "lgbm_pipeline_old",
}

NEW_MODEL_IDS = {"catboost_pipeline", "lgbm_pipeline"}

@asynccontextmanager
async def lifespan(_: FastAPI):
    MODELS_DIR.mkdir(exist_ok=True, parents=True)
    print("Приложение запущено")

    # Очищаем старые записи
    shared_state["models"].clear()

    # Подгружаем все .pkl из папки
    for model_file in MODELS_DIR.glob("*.pkl"):
        model_id = model_file.stem
        shared_state["models"][model_id] = {
            "model_path": str(model_file),
            "params": {},
            "metrics": {"r2": 0.0},
        }
        print(f"Подгружена модель: {model_id}")

    # Устанавливаем первую модель активной, если ещё нет
    if shared_state["active_model_id"] is None and shared_state["models"]:
        shared_state["active_model_id"] = next(iter(shared_state["models"]))
        print("Активная модель:", shared_state["active_model_id"])

    yield

    # По завершении — удаляем все .pkl кроме стандартных
    print("Начата процедура очистки нестандартных моделей...")
    for model_file in MODELS_DIR.glob("*.pkl"):
        model_name = model_file.stem  # без .pkl
        if model_name not in STANDARD_MODELS:
            try:
                model_file.unlink()
                print(f"Удалена нестандартная модель: {model_file.name}")
            except Exception as e:
                print(f"Ошибка при удалении {model_file.name}: {e}")
    print("Очистка завершена")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для разработки разрешаем все домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/fit/json", response_model=dict)
async def fit_json(request: FitRequestJson = Body(...), query_params: FitRequestQueryParams = Depends()):
    """Обучает модель на данных в формате JSON
    с поддержкой разных форматов параметров:
    1. JSON в теле запроса
    2. XML в теле запроса
    3. Query-параметры

    Возвращает:
        dict: Результат обучения с метриками и статусом
    """
    df = pd.DataFrame([item.model_dump() for item in request.data])

    # только для новых моделей добавляем фичи
    active_id = shared_state["active_model_id"]
    if active_id in NEW_MODEL_IDS:
        df = prepare_new_features(df)

    # собираем параметры обучения
    raw = request.params.model_dump() if request.params else {}
    if request.xml_params:
        try:
            doc = xmltodict.parse(request.xml_params)
            p = doc.get("params")
            if not p:
                raise ValueError("Не найден тег <params>")
            raw.update(p)
        except (ExpatError, ValueError) as e:
            raise HTTPException(422, f"Ошибка парсинга XML: {e}") from e

    for k, v in {
        "alpha": query_params.alpha,
        "max_iter": query_params.max_iter,
        "solver": query_params.solver,
    }.items():
        if v is not None:
            raw[k] = v

    return _start_training(df, raw, shared_state)


@app.post("/fit/csv", response_model=dict)
async def fit_csv(
    file: UploadFile = File(...),
    params_json: str = Form("{}"),
    query_params: FitRequestQueryParams = Depends(),
    xml_params: Optional[str] = Body("")
):
    """Обучает модель на данных в формате CSV
    с поддержкой разных форматов параметров:
    1. JSON(params_json)
    2. XML(xml_params)
    3. Query-параметры

    Возвращает:
        dict: Результат обучения с метриками и статусом
    """
    df = check_csv_file(file)

    active_id = shared_state["active_model_id"]
    if active_id in NEW_MODEL_IDS:
        df = prepare_new_features(df)

    try:
        raw = json.loads(params_json)
    except json.JSONDecodeError as e:
        raise HTTPException(422, f"Ошибка чтения JSON-параметров: {e}") from e

    try:
        validated_params = HyperParams(**raw).model_dump()
    except ValidationError as e:
        raise HTTPException(422, f"Ошибка проверки параметров: {e.errors()}") from e

    if xml_params:
        try:
            doc = xmltodict.parse(xml_params)
            p = doc.get("params")
            if not p:
                raise ValueError("Не найден тег <params>")
            validated_params.update(p)
        except (ExpatError, ValueError) as e:
            raise HTTPException(422, f"Ошибка парсинга XML: {e}") from e

    for k, v in {
        "alpha": query_params.alpha,
        "max_iter": query_params.max_iter,
        "solver": query_params.solver,
    }.items():
        if v is not None:
            validated_params[k] = v

    return _start_training(df, validated_params, shared_state)


@app.post("/predict/csv", response_model=List[float])
def predict_csv(file: UploadFile = File(...)):
    model_path = get_active_model_path(shared_state)
    df = check_csv_file(file)

    active_id = shared_state["active_model_id"]
    if active_id in NEW_MODEL_IDS:
        df = prepare_new_features(df)

    try:
        model = joblib.load(model_path)
        predictions = model.predict(df)
        return predictions.tolist()
    except Exception as e:
        tb = traceback.format_exc()
        print("Ошибка прогнозирования:\n", tb)
        raise HTTPException(500, detail=str(e)) from e


@app.get("/models", response_model=List[ModelInfo])
def get_models():
    """Получение списка всех моделей"""
    return [
        ModelInfo(
            id=model_id,
            name=f"Model-{model_id[:4]}",
            params=details.get("params", {}),
            metrics=details.get("metrics", {}),
        )
        for model_id, details in shared_state["models"].items()
    ]


@app.post("/models/{model_id}/set", response_model=dict)
def set_active_model(model_id: str):
    """Установка активной модели"""
    if model_id not in shared_state["models"]:
        raise HTTPException(status_code=404, detail="Модель не найдена")

    shared_state["active_model_id"] = model_id
    print("Активная модель установлена:", model_id)
    return {"status": "success", "active_model_id": model_id}


@app.post("/predict/csv", response_model=List[float])
def predict_csv(file: UploadFile = File(...)):
    """Выполнение предсказаний на данных в CSV-формате

    На вход подается:
        data: csv-файл с характеристиками автомобилей

    Возвращается:
        List[float]: Список предсказанных цен
    """
    model_path = get_active_model_path(shared_state)
    df = check_csv_file(file)

    active_id = shared_state["active_model_id"]
    if active_id in NEW_MODEL_IDS:
        df = prepare_new_features(df)

    try:
        model = joblib.load(model_path)
        predictions = model.predict(df)
        return predictions.tolist()
    except Exception as e:
        raise HTTPException(500, detail=str(e)) from e


@app.post("/predict/json", response_model=List[float])
async def predict_json(data: List[CarFeatures] = Body(...)):
    """Выполнение предсказаний на данных в JSON-формате

    На вход подается:
        data (List[CarFeatures]): Список объектов с характеристиками автомобилей

    Возвращается:
        List[float]: Список предсказанных цен
    """

    model_path = get_active_model_path(shared_state)
    df = pd.DataFrame([item.model_dump() for item in data])

    active_id = shared_state["active_model_id"]
    if active_id in NEW_MODEL_IDS:
        df = prepare_new_features(df)

    try:
        model = joblib.load(model_path)
        predictions = model.predict(df)
        return predictions.tolist()
    except Exception as e:
        raise HTTPException(500, detail=str(e)) from e