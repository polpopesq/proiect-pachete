import streamlit as st
from modules.load_data import load_ufo_data
from modules.preprocessing import preprocess_data
from modules.visualisation import show_top_cities, show_month_distribution, show_map

class VisualizationPage:
    def __init__(self):
        self.icon = "📊"
        self.title = "Vizualizări UFO"

    def __call__(self):
        st.title(self.icon + " " + self.title)
        data = load_ufo_data('data/ufo_us_sample.csv')
        data = preprocess_data(data)

        st.subheader("Top Orașe")
        show_top_cities(data)

        st.subheader("Distribuție pe Luni")
        show_month_distribution(data)

        st.subheader("Hartă Observații")
        show_map(data)
