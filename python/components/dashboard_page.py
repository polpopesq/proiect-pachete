import streamlit as st
import pandas as pd

class DashboardPage:
    def __init__(self, data):
        self.data = data

    def __call__(self):
        data = self.data.copy()

        st.title("Dashboard General")

        total_obs = len(data)
        st.metric("Numar total de observatii:", f"{total_obs:,}")

        st.subheader("Date raw")
        st.dataframe(data)

        st.divider()

        st.subheader("Distributie temporala")

        col1, col2 = st.columns(2)

        with col1:
            st.bar_chart(data['year'].value_counts().sort_index(), height=250, use_container_width=True)
            st.caption("Observatii pe ani")

        with col2:
            st.bar_chart(data['month'].value_counts().sort_index(), height=250, use_container_width=True)
            st.caption("Observatii pe luni")

        st.bar_chart(data['hour'].value_counts().sort_index(), height=250, use_container_width=True)
        st.caption("Observatii pe ore")

        st.divider()

        st.subheader("Durata medie a observatiilor")
        if 'duration (seconds)' in data.columns:
            avg_duration = data['duration (seconds)'].mean()
            st.metric("Durata medie", f"{avg_duration:.0f} secunde | {avg_duration/60:.2f} minute")

        st.divider()

        st.subheader("Cele mai raportate forme")
        if 'shape_grouped' in data.columns:
            shape_counts = data['shape_grouped'].value_counts()
        elif 'shape' in data.columns:
            shape_counts = data['shape'].value_counts()
        else:
            shape_counts = pd.Series()

        if not shape_counts.empty:
            st.bar_chart(shape_counts.head(10), height=300, use_container_width=True)
        else:
            st.info("Nu exista date despre forme")
