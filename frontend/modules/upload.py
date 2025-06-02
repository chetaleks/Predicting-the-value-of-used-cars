import streamlit as st
import pandas as pd


def run():
    """
    Streamlit-страница «Upload»: загрузка CSV и сохранение его в session_state.
    """
    st.header("Загрузка датасета")
    uploaded_file = st.file_uploader("Выберите CSV-файл с данными", type=["csv"])
    if not uploaded_file:
        st.info("Пожалуйста, загрузите CSV-файл")
        return
    df = pd.read_csv(uploaded_file)
    st.success("Файл загружен успешно!")
    st.subheader("Первые строки данных")
    st.dataframe(df.head())
    st.subheader("Статистика признаков")
    st.write(df.describe())
    st.session_state.df = df
