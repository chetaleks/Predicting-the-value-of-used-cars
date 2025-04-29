import os
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000")
TIMEOUT = 10


def get_models():
    """GET /models"""
    resp = requests.get(f"{API_URL}/models", timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def set_model(model_id: int):
    """POST /models/{id}/set"""
    resp = requests.post(f"{API_URL}/models/{model_id}/set", timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def fit_model(params: dict):
    """POST /fit"""
    resp = requests.post(f"{API_URL}/fit", json=params, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def predict(features: dict):
    """POST /predict"""
    resp = requests.post(f"{API_URL}/predict", json=features, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()
