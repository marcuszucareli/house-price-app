import streamlit as st
from mlflow_client.registry import get_places

# Get countries and citites
@st.cache_data
def get_locations():
    return get_places()


def update_city():
    print('Update Cidade:')
    print(st.session_state['city'])


# Get list of available places
places = get_locations()

# Evaluate places output
if not places or not isinstance(places, dict):
    # st.error('error')
    a, b = st.columns(2, vertical_alignment='center')
    with a:
        st.markdown(
            """
            # We are sorry...

            It looks like our servers are not working right now.

            Try to refresh the page in a few moments.
            """)
    with b:
        st.image("https://cdn-icons-png.flaticon.com/512/9068/9068699.png")
    
    st.markdown("---")
    st.html(
        '<a href="https://www.flaticon.com/free-icons/close" title="close icons">Close icons created by Fathema Khanom - Flaticon</a>'
    )
    
    st.stop()

# Add empty selection to the countries options list
countries = [''] + list(places.keys())

# Initiate city var
if "city" not in st.session_state:
    st.session_state.city = ''

# Welcome message
st.markdown("""
# Welcome to the World Real Estate Evaluator!

In this app, you can evaluate properties from various cities around the world!
            
Start by choosing a **country**.
""")

# Country selectbox
st.selectbox('Country', countries, key='country')

# City selectbox
if st.session_state['country'] != '':
    st.markdown('Now choose a **city**')
    st.selectbox('City', [''] + places[st.session_state['country']], on_change=update_city, key='city')

# Input model parameters
if st.session_state['city'] != '':
    st.markdown('Now fill the details about the property you want to evaluate bellow.')
