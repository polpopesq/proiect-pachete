import numpy as np
import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pydeck as pdk
from pathlib import Path

state_abbr_to_name = {
    'al': 'alabama', 'ak': 'alaska', 'az': 'arizona', 'ar': 'arkansas', 'ca': 'california',
    'co': 'colorado', 'ct': 'connecticut', 'de': 'delaware', 'fl': 'florida', 'ga': 'georgia',
    'hi': 'hawaii', 'id': 'idaho', 'il': 'illinois', 'in': 'indiana', 'ia': 'iowa', 'ks': 'kansas',
    'ky': 'kentucky', 'la': 'louisiana', 'me': 'maine', 'md': 'maryland', 'ma': 'massachusetts',
    'mi': 'michigan', 'mn': 'minnesota', 'ms': 'mississippi', 'mo': 'missouri', 'mt': 'montana',
    'ne': 'nebraska', 'nv': 'nevada', 'nh': 'new hampshire', 'nj': 'new jersey', 'nm': 'new mexico',
    'ny': 'new york', 'nc': 'north carolina', 'nd': 'north dakota', 'oh': 'ohio', 'ok': 'oklahoma',
    'or': 'oregon', 'pa': 'pennsylvania', 'ri': 'rhode island', 'sc': 'south carolina', 'sd': 'south dakota',
    'tn': 'tennessee', 'tx': 'texas', 'ut': 'utah', 'vt': 'vermont', 'va': 'virginia',
    'wa': 'washington', 'wv': 'west virginia', 'wi': 'wisconsin', 'wy': 'wyoming',
    'dc': 'district of columbia'
}


class VisualisationPage:
    def __init__(self, data):
        self.icon = "🗺️"
        self.title = "Analiză Geografică"
        self.data = data

    def __call__(self):
        st.title(f"{self.icon} {self.title}")
        df = self.data.copy()

        st.subheader("🇺🇸 Choropleth: Număr observații pe state")

        # Conversie în nume state
        df['state_full'] = df['state'].str.lower().map(state_abbr_to_name)

        # Număr observații pe state
        state_counts = df['state_full'].value_counts().reset_index()
        state_counts.columns = ['state_name', 'count']

        # Încarcă fișierul GeoJSON
        shp_path = Path("data/us_states.geojson")
        if not shp_path.exists():
            st.error("⚠️ Fișierul cu harta statelor SUA nu a fost găsit.")
            return

        states = gpd.read_file(shp_path)
        states['state'] = states['NAME'].str.lower()

        # Combină datele (join pe numele statului)
        states_merged = states.merge(state_counts, how="left", left_on='state', right_on='state_name')
        states_merged['count'] = states_merged['count'].fillna(0)

        # Plot choropleth
        fig, ax = plt.subplots(figsize=(10, 6))
        states_merged.plot(column='count', cmap='Reds', linewidth=0.8, edgecolor='0.8', ax=ax, legend=True)
        ax.set_title("Observații UFO pe state")
        ax.axis("off")
        st.pyplot(fig)

        st.divider()

        st.subheader("📍 Hartă interactivă cu observații")
        st.map(df[['latitude', 'longitude']])

        st.divider()

        st.subheader("🔥 Zone fierbinți: Clusterizare locații")
        try:
            k = st.slider("Număr de clustere:", min_value=2, max_value=10, value=4)
            coords = df[['latitude', 'longitude']]
            kmeans = KMeans(n_clusters=k, random_state=42)
            df['cluster'] = kmeans.fit_predict(coords)

            # Generăm culori unice pentru fiecare cluster
            colors = np.array([
                [255, 0, 0],  # roșu
                [0, 255, 0],  # verde
                [0, 0, 255],  # albastru
                [255, 255, 0],  # galben
                [255, 0, 255],  # magenta
                [0, 255, 255],  # cyan
                [255, 165, 0],  # portocaliu
                [128, 0, 128],  # mov
                [0, 128, 0],  # verde închis
                [128, 128, 0]  # olive
            ])
            df['color'] = df['cluster'].apply(lambda x: colors[x % len(colors)].tolist())

            # Creare hartă
            layer = pdk.Layer(
                'ScatterplotLayer',
                data=df,
                get_position='[longitude, latitude]',
                get_color='color',
                get_radius=10000,
                pickable=True
            )

            view_state = pdk.ViewState(
                longitude=df['longitude'].mean(),
                latitude=df['latitude'].mean(),
                zoom=3,
                pitch=0
            )

            st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

        except Exception as e:
            st.warning(f"Eroare la clusterizare: {e}")
