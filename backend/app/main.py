import json
import sys
import uuid
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

from .helper import check_csv_file, get_active_model_path
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

manager = Manager()
shared_state = manager.dict()
shared_state["models"] = manager.dict()
shared_state["active_model_id"] = None

@asynccontextmanager
async def lifespan(_: FastAPI):
    """Контекстный менеджер жизненного цикла приложения
    -Сначала создаем директории `models` и `logs`, если их нет.
    -Загружаем предварительно обученную модель из `models/final_model.pkl`
    -Если нет модели создаем новую модель `Ridge()` и сохраняем"""
    try:
        MODELS_DIR.mkdir(exist_ok=True, parents=True)
        print("Приложение запущено")

        initial_model_path = MODELS_DIR  / "final_model.pkl"

        if initial_model_path.exists():
            # Загрузка предобученной модели
            model = joblib.load(initial_model_path)
            print(f"Загружена начальная модель из {str(initial_model_path.absolute())}")
        else:
            # Создание новой модели, если файла нет
            model = Ridge()
            joblib.dump(model, initial_model_path)
            print("Создана новая начальная модель, так как final_model.pkl не найден")

        # Генерируем уникальный id, сохраняем в `shared_state`,
        # путь к файлу модели, параметры и метрики

        initial_model_id = str(uuid.uuid4())
        shared_state["models"][initial_model_id] = {
            "model_path": str(initial_model_path),
            "params": getattr(model, "params", {}),
            "metrics": getattr(model, "metrics", {"r2": 0.0}),
        }

        shared_state["active_model_id"] = initial_model_id

        print("Приложение успешно запущено")

    except Exception as e:
        print("Ошибка:", str(e))
        raise

    yield

    # После завершения работы,
    # удаляем все модели и информацию о них, кроме изначальной

    try:
        print("Начата процедура очистки...")

        for model_id in list(shared_state["models"].keys()):
            model_path = Path(shared_state["models"][model_id].get("model_path", ""))
            if model_path.exists() and model_path.name != "final_model.pkl":
                try:
                    model_path.unlink()
                    print("Удалена модель:", str(model_path))
                except Exception as e:
                    print("Ошибка удаления:", str(model_path), e)

        shared_state["models"].clear()
        print("Работа приложения остановлена")

    except Exception as e:
        print("Ошибка при очистке:", e)
        raise


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
    #
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
    xml_params: Optional[str] = Body(""),
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

    try:
        raw = json.loads(params_json)
    except json.JSONDecodeError as e:
        raise HTTPException(422, f"Ошибка чтения JSON-параметров: {e}") from e

    try:
        print(raw)
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

    try:
        model = joblib.load(model_path)
        predictions = model.predict(df)
        return predictions.tolist()

    except Exception as e:
        print("Ошибка прогнозирования:", str(e))
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

    print(df.columns)

    try:
        model = joblib.load(model_path)
        print("Шаги пайплайна:", model.named_steps.keys())
        predictions = model.predict(df)
        return predictions.tolist()

    except Exception as e:
        print("Ошибка прогнозирования:", str(e))
        raise HTTPException(500, detail=str(e)) from e
