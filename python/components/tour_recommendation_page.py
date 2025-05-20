import streamlit as st
import altair as alt
import pydeck as pdk
from modules.train_model import run_simple_logistic
from modules.optimal_route import compute_optimal_route, show_route_map

class TourRecommendationPage:
    def __init__(self, data):
        self.df_clean, self.X, self.y, self.model = run_simple_logistic(data)

        self.df_clean['hotspot_prob'] = self.model.predict_proba(self.X)[:, 1]

        self.location_probs = (
            self.df_clean.groupby(['city', 'state'])
            .agg(
                avg_probability=('hotspot_prob', 'mean'),
                latitude=('latitude', 'mean'),
                longitude=('longitude', 'mean')
            )
            .reset_index()
            .sort_values('avg_probability', ascending=False)
        )

    def __call__(self):
        st.title("Recomandari tururi OZN")
        st.markdown("Top locatii cu cea mai mare probabilitate de aparitie OZN")

        location_probs = self.location_probs.copy()
        location_probs['probabilitate_fmt'] = (location_probs['avg_probability'] * 100).map(lambda x: f"{x:.2f}%")
        location_probs['tooltip_html'] = (
            "<b>Oras:</b> " + location_probs['city'].fillna("necunoscut") + "<br>" +
            "<b>Stat:</b> " + location_probs['state'].fillna("necunoscut") + "<br>" +
            "<b>Latitudine:</b> " + location_probs['latitude'].round(4).astype(str) + "<br>" +
            "<b>Longitudine:</b> " + location_probs['longitude'].round(4).astype(str) + "<br>" +
            "<b>Probabilitate:</b> " + location_probs['probabilitate_fmt']
        )

        location_probs['color'] = location_probs['avg_probability'].apply(
            lambda x: [255, int(255 * (1 - x)), int(255 * (1 - x))]
        )

        st.subheader("Vizualizare grafica")
        chart = alt.Chart(location_probs.head(10)).mark_bar().encode(
            x=alt.X('avg_probability:Q', title='Probabilitate medie'),
            y=alt.Y('city:N', sort='-x', title='Oraș'),
            color=alt.Color('avg_probability:Q', scale=alt.Scale(scheme='reds'))
        ).properties(height=400)
        st.altair_chart(chart, use_container_width=True)

        st.subheader("Harta interactiva")
        tooltip = {
            "html": "{tooltip_html}",
            "style": {
                "backgroundColor": "white",
                "color": "black",
                "fontSize": "13px",
                "padding": "8px",
                "borderRadius": "5px"
            }
        }

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=location_probs,
            get_position="[longitude, latitude]",
            get_radius=50000,
            get_color="color",
            pickable=True
        )

        view_state = pdk.ViewState(
            latitude=location_probs["latitude"].mean(),
            longitude=location_probs["longitude"].mean(),
            zoom=3,
            pitch=0
        )

        st.pydeck_chart(pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip=tooltip
        ))

        st.markdown("""
        <style>
        .color-bar-wrapper {
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        .color-bar {
            height: 20px;
            background: linear-gradient(to right, white, red);
            border: 1px solid #ccc;
        }
        .color-bar-labels {
            display: flex;
            justify-content: space-between;
            font-size: 0.9rem;
            margin-top: 0.2rem;
            color: #333;
        }
        </style>

        <div class="color-bar-wrapper">
            <div class="color-bar"></div>
            <div class="color-bar-labels">
                <span>0.0</span>
                <span>0.25</span>
                <span>0.50</span>
                <span>0.75</span>
                <span>1.0</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("Tur recomandat")
        route_df = compute_optimal_route(location_probs, top_n=10)
        st.dataframe(route_df)

        st.subheader("Harta traseului recomandat")
        show_route_map(route_df)
