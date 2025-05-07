import streamlit as st
import pandas as pd
import numpy as np
from api_client import get_models, set_model, predict_json, predict_csv

"""
Страница «Predict»: рисует форму с полями CarFeatures или
позволяет загрузить CSV для пакетного предсказания.
"""
FEATURE_FIELDS = [
    ("production_year", int, 2020),
    ("mileage", int, 50000),
    ("condition", str, ""),
    ("owners_number", int, 1),
    ("pts_original", bool, False),
    ("accidents_resolution", str, ""),
    ("region", str, ""),
    ("seller_type", str, ""),
    ("brand", str, ""),
    ("model", str, ""),
    ("body_type", str, ""),
    ("doors_count", int, 4),
    ("seats", int, 5),
    ("engine_displacement", float, 1.5),
    ("engine_power", float, 100.0),
    ("fuel_rate", float, 8.0),
    ("steering_wheel", str, ""),
    ("price", float, 0.0),
    ("price_segment", str, ""),
    ("auto_class", str, ""),
    ("horse_power", int, 100),
    ("tags", str, ""),
    ("equipment", str, ""),
    ("complectation_available_options", str, ""),
]


def run():
    """
    Streamlit-страница «Predict»:
    1. Получает список моделей с бэкенда и позволяет
       установить активную модель.
    2. Дает выбор режима инференса:
       – одиночный JSON-ввод всех полей CarFeatures;
       – пакетный ввод через CSV-файл.
    3. Отправляет запросы к эндпоинтам /predict/json или /predict/csv
       и отображает результат (список предсказанных цен).
    """
    st.header("Предсказание цены")

    # Выбор модели
    models = get_models()
    model_map = {m["name"]: m["id"] for m in models}
    choice = st.selectbox("Выберите модель", list(model_map.keys()))
    if st.button("Установить модель"):
        set_model(model_map[choice])
        st.success(f"Активная модель: {choice}")

    # Режим предсказания
    mode = st.radio(
        "Режим предсказания", ["Одно значение (формой)", "Пакетный CSV"], index=0
    )

    if mode == "Одно значение (формой)":
        features = {}
        for name, typ, default in FEATURE_FIELDS:
            label = name.replace("_", " ").title()
            if typ == int:
                features[name] = st.number_input(label, value=default, step=1)
            elif typ == float:
                features[name] = st.number_input(label, value=default, format="%f")
            elif typ == bool:
                features[name] = st.checkbox(label, value=default)
            else:
                features[name] = st.text_input(label, value=default)

        if st.button("Predict (JSON)"):
            with st.spinner("Предсказываем…"):
                try:
                    prices = predict_json(features)
                    st.success(f"Цена: {prices[0]:.2f}")
                except Exception as e:
                    st.error(f"Ошибка предсказания: {e}")
    else:
        uploaded_file = st.file_uploader(
            "Загрузите CSV для пакетного предсказания", type=["csv"]
        )
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            df = df.replace([np.inf, -np.inf], np.nan).fillna(0)
            if st.button("Predict (CSV)"):
                with st.spinner("Пакетное предсказание…"):
                    try:
                        res = predict_csv(df)
                        st.write("Результаты:")
                        st.dataframe(res)
                    except Exception as e:
                        st.error(f"Ошибка пакетного предсказания: {e}")
