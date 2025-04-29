import streamlit as st
from api_client import get_models, set_model, predict

def run():
    st.header("Предсказание цены")
    models = get_models()
    model_map = {m['name']: m['id'] for m in models}
    choice = st.selectbox("Выберите модель", list(model_map.keys()))
    if st.button("Установить модель"):
        set_model(model_map[choice])
        st.success(f"Активная модель: {choice}")

    st.subheader("Характеристики машины")
    mileage = st.number_input("Пробег (км)", min_value=0, value=50000)
    year = st.number_input("Год выпуска", min_value=1900, max_value=2025, value=2015)
    if st.button("Predict"):
        features = {"mileage": mileage, "year": year}
        res = predict(features)
        st.success(f"Predicted price: {res.get('price'):.2f}")
