import streamlit as st
from modules.load_data import load_ufo_data
from modules.preprocessing import preprocess_data
from modules.clustering import perform_clustering
from modules.visualisation import show_map

class ClusteringPage:
    def __init__(self):
        self.icon = "🔵"
        self.title = "Clusterizare Locații UFO"

    def __call__(self):
        st.title(self.icon + " " + self.title)
        data = load_ufo_data('data/ufo_us_sample.csv')
        data = preprocess_data(data)
        data_clustered = perform_clustering(data)

        st.subheader("Date cu clustere")
        st.dataframe(data_clustered[['city', 'state', 'cluster']])

        st.subheader("Hartă cu Clustere")
        show_map(data_clustered)
