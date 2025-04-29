import streamlit as st
from api_client import fit_model, get_models

def run():
    st.header("Обучение модели")
    lr = st.number_input("Learning rate", min_value=0.0001, max_value=1.0, value=0.01, step=0.01)
    epochs = st.number_input("Количество эпох", min_value=1, max_value=100, value=10, step=1)
    btn = st.button("Запустить обучение")
    if btn:
        params = {"learning_rate": lr, "epochs": int(epochs)}
        st.info("Запускаем обучение...")
        res = fit_model(params)
        st.success(f"Обучение запущено! exp_id = {res.get('exp_id')}")
        models = get_models()
        st.write("Доступные модели:", models)

