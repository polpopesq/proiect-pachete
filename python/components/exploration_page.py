from pathlib import Path

import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

class ExplorationPage:
    def __init__(self, data):
        self.icon = "🔍"
        self.title = "Explorare Avansată"
        self.data = data

    def __call__(self):
        st.title(f"{self.icon} {self.title}")
        df = self.data.copy()

        st.sidebar.header("🔧 Filtre disponibile")

        # ✅ Filtrare după stat
        state_options = df['state'].dropna().unique()
        selected_state = st.sidebar.multiselect("Selectează state:", sorted(state_options))

        if selected_state:
            df = df[df['state'].isin(selected_state)]

        # ✅ Filtrare după oraș
        city_options = df['city'].dropna().unique()
        selected_city = st.sidebar.multiselect("Selectează orașe:", sorted(city_options))

        if selected_city:
            df = df[df['city'].isin(selected_city)]

        # ✅ Filtrare după formă (shape_grouped dacă există, altfel shape)
        shape_col = 'shape_grouped' if 'shape_grouped' in df.columns else 'shape'
        shape_options = df[shape_col].dropna().unique()
        selected_shape = st.sidebar.multiselect("Selectează forme (shape):", sorted(shape_options))

        if selected_shape:
            df = df[df[shape_col].isin(selected_shape)]

        # ✅ Filtrare după durată
        if 'duration (seconds)' in df.columns:
            min_dur = int(df['duration (seconds)'].min())
            max_dur = int(df['duration (seconds)'].max())
            selected_dur = st.sidebar.slider("Durata (secunde):", min_value=min_dur, max_value=max_dur, value=(min_dur, max_dur))
            df = df[df['duration (seconds)'].between(*selected_dur)]

        # ✅ Filtrare după anotimp
        if 'month' in df.columns:
            season_mapping = {
                "Primăvară": [3, 4, 5],
                "Vara": [6, 7, 8],
                "Toamna": [9, 10, 11],
                "Iarna": [12, 1, 2]
            }
            selected_seasons = st.sidebar.multiselect("Selectează anotimpuri:", list(season_mapping.keys()))
            if selected_seasons:
                selected_months = [m for s in selected_seasons for m in season_mapping[s]]
                df = df[df['month'].isin(selected_months)]

        # 📊 Afișare rezultate filtrate
        st.subheader("📋 Rezultate filtrate")
        st.write(f"{len(df):,} observații găsite.")
        st.dataframe(df)

        st.divider()
        st.subheader("🗺️ Hartă observații")
        if 'latitude' in df.columns and 'longitude' in df.columns:
            location_data = df[['latitude', 'longitude']].dropna()
            st.map(location_data)

        # 🔽 Export
        st.download_button("⬇️ Descarcă datele filtrate", df.to_csv(index=False), file_name="ufo_filtrat.csv", mime="text/csv")
