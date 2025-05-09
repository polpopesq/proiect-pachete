import streamlit as st
import pandas as pd

class ExplorationPage:
    def __init__(self, data):
        self.data = data

    def __call__(self):
        st.title("Filtrare & Explorare")
        df = self.data.copy()

        st.sidebar.header("Filtre")

        state_options = df['state'].dropna().unique()
        selected_state = st.sidebar.multiselect("Selecteaza statele:", sorted(state_options))

        if selected_state:
            df = df[df['state'].isin(selected_state)]

        city_options = df['city'].dropna().unique()
        selected_city = st.sidebar.multiselect("Selecteaza orasele:", sorted(city_options))

        if selected_city:
            df = df[df['city'].isin(selected_city)]

        shape_col = 'shape_grouped' if 'shape_grouped' in df.columns else 'shape'
        shape_options = df[shape_col].dropna().unique()
        selected_shape = st.sidebar.multiselect("Selecteaza formele:", sorted(shape_options))

        if selected_shape:
            df = df[df[shape_col].isin(selected_shape)]

        if 'duration (seconds)' in df.columns:
            df['duration (seconds)'] = pd.to_numeric(df['duration (seconds)'], errors='coerce')

            x = df['duration (seconds)'].nlargest(200).min()

            min_dur = 0
            max_dur = int(x)

            selected_dur = st.sidebar.slider(
                "Durata (secunde):",
                min_value=min_dur,
                max_value=max_dur,
                value=(min_dur, max_dur)
            )

            df = df[df['duration (seconds)'].between(*selected_dur)]

        if 'month' in df.columns:
            season_mapping = {
                "Primavara": [3, 4, 5],
                "Vara": [6, 7, 8],
                "Toamna": [9, 10, 11],
                "Iarna": [12, 1, 2]
            }
            selected_seasons = st.sidebar.multiselect("Selecteaza anotimpurile:", list(season_mapping.keys()))
            if selected_seasons:
                selected_months = [m for s in selected_seasons for m in season_mapping[s]]
                df = df[df['month'].isin(selected_months)]

        st.subheader("Rezultate filtrate")
        st.write(f"{len(df):,} observatii gasite.")
        st.dataframe(df)

        st.divider()
        st.subheader("Harta observatiilor filtrate")
        if 'latitude' in df.columns and 'longitude' in df.columns:
            location_data = df[['latitude', 'longitude']].dropna()
            st.map(location_data)

        st.download_button("Descarca datele filtrate", df.to_csv(index=False), file_name="ufo_filtrat.csv", mime="text/csv")
