import streamlit as st
import pandas as pd
import plotly.express as px

def run():
    st.header("EDA / Анализ данных")
    df = st.session_state.get('df')
    if df is None:
        st.info("Сначала загрузите датасет на странице Upload")
        return
    numeric_cols = df.select_dtypes(include=['int64','float64']).columns.tolist()
    col = st.selectbox("Выберите признак для гистограммы", numeric_cols)
    fig = px.histogram(df, x=col, nbins=30, title=f"Гистограмма {col}")
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("Scatter Plot")
    x = st.selectbox("X-ось", numeric_cols, index=0)
    y = st.selectbox("Y-ось", numeric_cols, index=1)
    fig2 = px.scatter(df, x=x, y=y, title=f"{y} vs {x}")
    st.plotly_chart(fig2, use_container_width=True)
    st.subheader("Корреляционная матрица")
    corr = df[numeric_cols].corr()
    fig3 = px.imshow(corr, text_auto=True, title="Корреляция признаков")
    st.plotly_chart(fig3, use_container_width=True)
    
   