import streamlit as st
from mlflow_client.registry import Models

# Get countries and citites
@st.cache_data
def get_models():
    return Models()


def update_city():
    if st.session_state['city'] != '':
        inputs = models.get_inputs(st.session_state['city'])
        st.session_state['inputs'] = inputs

        for input, data in st.session_state['inputs'].items():
            if input in st.session_state:
                match data['type']:
                    case 'categorical':
                        st.session_state[input] = data['options'][0]
                    case 'bool':
                        st.session_state[input] = False
                    case 'int':
                        st.session_state[input] = 0
                    case 'float':
                        st.session_state[input] = 0
    else:
        st.session_state['inputs'] = {}


# Get list of available places
models = get_models()

places = models.get_places()

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

# Initiate city and inputs variales
if "city" not in st.session_state:
    st.session_state.city = ''
if 'inputs' not in st.session_state:
    st.session_state.inputs = {}

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
if st.session_state['city'] != '' and \
    st.session_state['country'] != '':
    st.markdown('Now fill the details about the property you want to evaluate bellow.')

    for input, data in st.session_state['inputs'].items():
        match data['type']:
            case 'categorical':
                st.selectbox(data['name'], data['options'], key=input)
            case 'bool':
                st.toggle(data['name'], value=False, key=input)
            case 'int':
                st.number_input(data['name'], step=1, key=input, min_value=0)
            case 'float':
                st.number_input(data['name'], step=.01, key=input, min_value=0.00)