import streamlit as st
import pandas as pd

class DashboardPage:
    def __init__(self, data):
        self.icon = "📊"
        self.title = "Dashboard General"
        self.data = data

    def __call__(self):
        data = self.data.copy()

        st.title(f"{self.icon} {self.title}")

        # 🧮 Număr total de observații
        total_obs = len(data)
        st.metric("Număr total observații", f"{total_obs:,}")

        st.subheader("Date raw")
        st.dataframe(data)

        st.divider()

        # 📆 Distribuție pe ani, luni, ore
        st.subheader("Distribuție temporală")

        col1, col2 = st.columns(2)

        with col1:
            st.bar_chart(data['year'].value_counts().sort_index(), height=250, use_container_width=True)
            st.caption("Observații pe ani")

        with col2:
            st.bar_chart(data['month'].value_counts().sort_index(), height=250, use_container_width=True)
            st.caption("Observații pe luni")

        st.bar_chart(data['hour'].value_counts().sort_index(), height=250, use_container_width=True)
        st.caption("Observații pe ore")

        st.divider()

        # ⏱️ Durată medie
        st.subheader("Durata medie a observațiilor")
        if 'duration (seconds)' in data.columns:
            avg_duration = data['duration (seconds)'].mean()
            st.metric("Durată medie", f"{avg_duration:.0f} secunde | {avg_duration/60:.2f} minute")

        st.divider()

        # 🛸 Cele mai raportate forme
        st.subheader("Cele mai raportate forme (shape)")
        if 'shape_grouped' in data.columns:
            shape_counts = data['shape_grouped'].value_counts()
        elif 'shape' in data.columns:
            shape_counts = data['shape'].value_counts()
        else:
            shape_counts = pd.Series()

        if not shape_counts.empty:
            st.bar_chart(shape_counts.head(10), height=300, use_container_width=True)
        else:
            st.info("Nu există date despre forme (shape).")
