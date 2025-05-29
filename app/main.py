import streamlit as st
from mlflow_client.registry import get_places

# Get countries and citites
@st.cache_data
def get_locations():
    return get_places()

places = get_locations()

st.markdown("""
# Welcome to the World Real Estate Evaluator!

In this app, you can evaluate properties from various cities.
""")

st.selectbox('Country', places.keys())
