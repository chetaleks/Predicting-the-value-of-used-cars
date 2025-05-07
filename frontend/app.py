import streamlit as st
from modules import upload, eda, train, predict

st.set_page_config(page_title="Car Price App", layout="wide")
st.sidebar.title("Навигация")
page = st.sidebar.radio(" ", ["Upload", "EDA", "Train", "Predict"])

if page == "Upload":
    upload.run()
elif page == "EDA":
    eda.run()
elif page == "Train":
    train.run()
elif page == "Predict":
    predict.run()
