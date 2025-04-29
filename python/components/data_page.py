import streamlit as st
from modules.load_data import load_ufo_data

class DataPage:
    def __init__(self):
        self.icon = "📄"
        self.title = "Date UFO Observații"

    def __call__(self):
        st.title(self.icon + " " + self.title)
        data = load_ufo_data('data/ufo_us_sample.csv')
        st.dataframe(data)
