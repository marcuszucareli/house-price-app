import streamlit as st

st.set_page_config(
    page_title="Results",
    page_icon="📊",
    initial_sidebar_state='collapsed'
)

st.markdown('# You are in results')
st.session_state['prediction']['value']