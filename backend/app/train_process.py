import uuid
from multiprocessing import Process
from pathlib import Path

import pandas as pd
from fastapi import HTTPException

from .model_trainer import ModelTrainer
from .schemas import HyperParams

from .paths import MODELS_DIR


# используется в main.py
def _start_training(df: pd.DataFrame, raw_params: dict, shared_state: dict):
    try:
        params = HyperParams(**raw_params).model_dump()
    except Exception as e:
        raise HTTPException(422, f"Ошибка валидации параметров: {e}") from e

    model_id = str(uuid.uuid4())
    p = Process(target=train_task, args=(df, params, model_id, shared_state))
    p.start()
    p.join(10)
    if p.is_alive():
        p.terminate()
        raise HTTPException(408, "Превышено время обучения")

    return {"model_id": model_id, "status": "started", "params": params}


def train_task(df: pd.DataFrame, validated_params: dict, model_id: str, shared_state: dict):
    """Функция для обучения модели в отдельном процессе"""
    try:
        print("Начато обучение модели", model_id)
        # Создаем папку для моделей если нет ее
        MODELS_DIR.mkdir(parents=True, exist_ok=True)

        trainer = ModelTrainer()
        result = trainer.train(df, validated_params)

        model_path = MODELS_DIR / f"{model_id}.joblib"
        trainer.save_model(model_path)

        shared_state["models"][model_id] = {
            "params": validated_params,
            "metrics": result.get("metrics", {}),
            "model_path": model_path,
        }

        print(f"Обучение модели {model_id} завершено")
    except Exception as e:
        print(f"Ошибка обучения модели {model_id}: {str(e)}")
        raise
