import streamlit as st

def show_top_cities(data):
    top_cities = data['city'].value_counts().head(10)
    st.bar_chart(top_cities)

def show_month_distribution(data):
    month_distribution = data['month'].value_counts().sort_index()
    st.line_chart(month_distribution)

def show_map(data):
    st.map(data[['latitude', 'longitude']])
