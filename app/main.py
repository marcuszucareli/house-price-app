import streamlit as st
from app.client import Models

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    initial_sidebar_state='collapsed' 
)

# Cache model
@st.cache_data
def get_models():
    return Models()
    
    
def update_country():
    st.session_state['model'].country = st.session_state['country']
    if st.session_state['model'].country != None:
        st.session_state['model'].get_cities()
    else:
        st.session_state['model'].cities = []
    st.session_state['model'].reset(
        st.session_state['model']._index['cities'])
    

def update_city():
    st.session_state['model'].city = st.session_state['city']
    if st.session_state['model'].city != None:
        st.session_state['model'].get_model()
        st.session_state['model'].get_inputs()

    else:
        st.session_state['model'].reset(
            st.session_state['model']._index['city'])


def submit():
    for key, item in st.session_state.items():
        print(key, item)
    # st.session_state['submited'] = True


# Check if submited was pressed
if 'submited' in st.session_state:
    del st.session_state.submited
    st.switch_page('pages/results.py')

# Get models instance
model = get_models()

if model != None:
    #  Initializa model
    if "model" not in st.session_state:
        st.session_state.model = model
        st.session_state['model'].countries = \
            [None] + st.session_state['model'].countries
else:
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

# Welcome message
st.markdown("""
# Welcome to the World Real Estate Evaluator!

In this app, you can evaluate properties from various cities around the world!
            
### Start by choosing a **country**:
""")

# Country selectbox
st.selectbox(
    'Country',
    st.session_state['model'].countries,
    on_change=update_country,
    key='country')

# City selectbox
if st.session_state['model'].country != None:
    st.markdown('### Choose a **city**:')
    st.selectbox(
        'City',
        [None] + st.session_state['model'].cities,
        on_change=update_city,
        key='city')

# Input model parameters
if st.session_state['model'].inputs != None:
    st.markdown('### Fill the details of your property:')

    with st.form('form_inputs', clear_on_submit=True):
        for input in st.session_state['model'].inputs:
            if input['unit'] in [None, '']:
                unit = ''
            else:
                unit = f'({input['unit']})'

            match input['type']:
                case 'categorical':
                    st.selectbox(
                        label=f'{input['label']} {unit}',
                        options=input['options'],
                        key=input['column_name'],
                        help=input['description']
                    )
                case 'bool':
                    st.toggle(
                        label=f'{input['label']} {unit}',
                        key=input['column_name'],
                        help=input['description']
                    )
                case 'int':
                    st.number_input(
                        label=f'{input['label']} {unit}',
                        key=input['column_name'],
                        help=input['description'],
                        step=1
                    )
                case 'float':
                    st.number_input(
                        label=f'{input['label']} {unit}',
                        key=input['column_name'],
                        help=input['description']
                    )
        
        st.form_submit_button('Evaluate My Property', on_click=submit, type='primary',use_container_width=True)