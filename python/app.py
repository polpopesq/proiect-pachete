import streamlit as st
from components.data_page import DataPage
from components.visualization_page import VisualizationPage
from components.clustering_page import ClusteringPage

# Setare pagină curentă în session_state dacă nu există deja
if "pagina_curenta" not in st.session_state:
    st.session_state.pagina_curenta = "Date"

# Funcții care schimbă pagina
def set_page(page_name):
    st.session_state.pagina_curenta = page_name

# Sidebar cu butoane
st.sidebar.title("Navigare")
st.sidebar.button("Date", on_click=set_page, args=("Date",))
st.sidebar.button("Vizualizări", on_click=set_page, args=("Vizualizări",))
st.sidebar.button("Clusterizare", on_click=set_page, args=("Clusterizare",))

# Dicționar de pagini
pages = {
    "Date": DataPage(),
    "Vizualizări": VisualizationPage(),
    "Clusterizare": ClusteringPage()
}

# Afișează pagina activă
pages[st.session_state.pagina_curenta]()
