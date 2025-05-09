import streamlit as st
from components.visualization_page import VisualisationPage
from components.dashboard_page import DashboardPage
from components.exploration_page import ExplorationPage
from modules.load_data import load_ufo_data
from modules.preprocessing import preprocess_data
from components.tour_recommendation_page import TourRecommendationPage

data = load_ufo_data()
data = preprocess_data(data)
data = data.dropna(subset=['duration (seconds)']) # somehow preprocess baga 2 NA uri pe duration(seconds), nu imi bat capul

if "pagina_curenta" not in st.session_state:
    st.session_state.pagina_curenta = "Dashboard"

def set_page(page_name):
    st.session_state.pagina_curenta = page_name

st.sidebar.title("Navigare")
st.sidebar.button("Dashboard", on_click=set_page, args=("Dashboard",))
st.sidebar.button("Explorare", on_click=set_page, args=("Explorare",))
st.sidebar.button("Harta", on_click=set_page, args=("Harta",))
st.sidebar.button("Tururi", on_click=set_page, args=("Recomandări Tururi",))


pages = {
    "Harta": VisualisationPage(data),
    "Dashboard": DashboardPage(data),
    "Explorare": ExplorationPage(data),
    "Recomandări Tururi": TourRecommendationPage(data)
}

pages[st.session_state.pagina_curenta]()
