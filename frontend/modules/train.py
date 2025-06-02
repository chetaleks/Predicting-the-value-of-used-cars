import streamlit as st
import pandas as pd
import numpy as np
import requests
from api_client import get_models, fit_model_json, fit_model_csv


def normalize_record(record: dict):
    """
    Приводит запись из DataFrame к JSON-совместимому виду:
    - заменяет NaN/inf на None,
    - numpy-типы на чистые Python int/float.
    """
    clean = {}
    for k, v in record.items():
        if v is None or (isinstance(v, float) and (np.isnan(v) or np.isinf(v))):
            clean[k] = None
        elif isinstance(v, (pd._libs.interval.Interval,)):
            clean[k] = str(v)
        elif hasattr(v, "tolist"):
            clean[k] = v.tolist()
        else:
            clean[k] = v
    return clean


def run():
    """
    Streamlit-страница «Train»: рисует UI для загрузки гиперпараметров
    и запускает обучение модели через API.
    С поддержкой двух режимов: JSON и CSV.
    """
    st.header("Обучение модели на вашем датасете")
    df = st.session_state.get("df")
    if df is None:
        st.info("Сначала загрузите датасет")
        return

    alpha = st.number_input("Alpha", value=1.0, step=0.1)
    max_iter = st.number_input("Max iter", value=100, step=10)
    solver = st.selectbox(
        "Solver",
        [
            "auto",
            "svd",
            "sag",
            "saga",
            "lbfgs",
            "sparse_cg",
            "lsqr",
            "cholesky",
        ],
        index=0,
    )

    mode = st.radio("Режим подачи данных", ["JSON-параметры", "CSV-файл"], index=0)

    if mode == "JSON-параметры":
        if st.button("Train (JSON)"):
            clean_df = df.replace([np.inf, -np.inf], np.nan)
            records = clean_df.where(pd.notnull(clean_df), None).to_dict(
                orient="records"
            )
            records = [normalize_record(rec) for rec in records]
            params = {"alpha": alpha, "max_iter": int(max_iter), "solver": solver}
            with st.spinner("Обучаем (JSON)…"):
                try:
                    res = fit_model_json(records, params)
                    st.success("Обучение запущено!")
                    st.json(res)
                except requests.HTTPError as e:
                    st.error(f"Ошибка обучения: {e.response.text}")
    else:
        st.write("Будет передан весь CSV-файл с query-параметрами")
        if st.button("Train (CSV)"):
            params = {"alpha": alpha, "max_iter": max_iter, "solver": solver}
            with st.spinner("Обучаем (CSV)…"):
                try:
                    res = fit_model_csv(df, params)
                    st.success("Обучение завершено!")
                    st.json(res)
                except requests.HTTPError as e:
                    st.error(f"Ошибка обучения: {e.response.text}")

    st.subheader("Доступные модели")
    st.write(get_models())
