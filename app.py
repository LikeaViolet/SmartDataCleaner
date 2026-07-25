
import streamlit as st

from src.ui.layout import render_app

st.set_page_config(
    page_title="Smart Data Cleaner",
    #page_icon="🧹",
    layout="wide",
)

render_app()