import os
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000")
TIMEOUT = 10


def get_models():
    resp = requests.get(f"{API_URL}/models", timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def set_model(model_id: int):
    resp = requests.post(f"{API_URL}/models/{model_id}/set", timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


# FIT via JSON (params in body)
def fit_model_json(df_records: list, params: dict):
    payload = {"data": df_records, "params": params, "xml_params": ""}
    resp = requests.post(f"{API_URL}/fit/json", json=payload, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def fit_model_csv(df, params: dict, xml_params: str = ""):
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
    payload = [features]
    resp = requests.post(f"{API_URL}/predict/json", json=payload, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def predict_csv(df):
    files = {"file": ("data.csv", df.to_csv(index=False).encode("utf-8"), "text/csv")}
    resp = requests.post(f"{API_URL}/predict/csv", files=files, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()
