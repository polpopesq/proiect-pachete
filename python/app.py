import streamlit as st
from components.visualization_page import VisualisationPage
from components.dashboard_page import DashboardPage
from components.exploration_page import ExplorationPage
from modules.load_data import load_ufo_data
from modules.preprocessing import preprocess_data
from modules.model_pipeline import run_pipeline
from components.tour_recommendation_page import TourRecommendationPage

data = load_ufo_data(raw=True)
data = preprocess_data(data)

#antrenare model predictie
print(data.columns)
data, X, y, model = run_pipeline(data)

# Setare pagină curentă în session_state dacă nu există deja
if "pagina_curenta" not in st.session_state:
    st.session_state.pagina_curenta = "Dashboard"

# Funcții care schimbă pagina
def set_page(page_name):
    st.session_state.pagina_curenta = page_name

# Sidebar cu butoane
st.sidebar.title("Navigare")
st.sidebar.button("Dashboard", on_click=set_page, args=("Dashboard",))
st.sidebar.button("Explorare", on_click=set_page, args=("Explorare",))
st.sidebar.button("Harta", on_click=set_page, args=("Harta",))
st.sidebar.button("Tururi", on_click=set_page, args=("Recomandări Tururi",))


# Dicționar de pagini
pages = {
    "Harta": VisualisationPage(data),
    "Dashboard": DashboardPage(data),
    "Explorare": ExplorationPage(data),
    "Recomandări Tururi": TourRecommendationPage(data, model)
}

# Afișează pagina activă
pages[st.session_state.pagina_curenta]()
