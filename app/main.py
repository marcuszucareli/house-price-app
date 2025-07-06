import streamlit as st
import folium
from streamlit_folium import st_folium
from app.client import Models
import requests


def get_city_coord(city: str):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city,
        "format": "json",
        "limit": 1
    }
    headers = {"User-Agent": "geo-app/1.0"}
    
    res = requests.get(url, params=params, headers=headers)
    if res.status_code != 200 or not res.json():
        coords = [0, 0]
        bbox = [[-60, -170], [75, 180]]
    else:
        data = res.json()
        city_data = data[0]
        bbox_raw = city_data["boundingbox"]
        coords = [float(city_data["lat"]), float(city_data["lon"])]
        bbox = [
            [float(bbox_raw[0]), float(bbox_raw[2])],  # [south, west]
            [float(bbox_raw[1]), float(bbox_raw[3])]   # [north, east]
        ]

    return {
        "coords": coords,
        "boundingbox": bbox,
        "zoom": 16
    }


def clamp_lng(lng):
    return max(-180, min(180, lng))


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
        
    if 'markers' in st.session_state:
        st.session_state.markers.clear()


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

# Input map
if st.session_state['model'].inputs != None:
    has_coordinates = any(item["type"] == "map" \
                    for item in st.session_state['model'].inputs)
else:
    has_coordinates = False

if has_coordinates:

    # Create session state only if we use map
    if 'markers' not in st.session_state:
        st.session_state.markers = []

    # Use boundary only when there's no selected marker (user input)
    use_bbox = False
    # Get city coords and boundaries
    if not st.session_state['markers']:
        # get boundaries from api
        city_data = get_city_coord(st.session_state.model.city)
        use_bbox = True
    else:
        # User marker and zoom option if user already selected the address
        city_data = st.session_state['markers'][0]

    coords = city_data['coords']
    bbox = city_data['boundingbox']
    zoom = city_data['zoom']

    m = folium.Map(location=coords, zoom_start=zoom)

    if use_bbox:
        m.fit_bounds(bbox)

    for marker in st.session_state.markers:
        folium.Marker(
            [
                marker['coords'][0],
                marker['coords'][1],
            ],
        ).add_to(m)

    # Render map
    st.markdown("""### Select the location of your home on the map""")
    st_data = st_folium(m, width=725)

    # Update map on click
    if st_data and st_data.get("last_clicked"):
        
        # Exlude previous marker
        st.session_state.markers.clear()

        # Set coords and boundary
        lat = st_data["last_clicked"]["lat"]
        lng = st_data["last_clicked"]["lng"]

        sw = st_data['bounds']["_southWest"]
        ne = st_data['bounds']["_northEast"]
        bbox = [
            [sw["lat"], clamp_lng(sw["lng"])],
            [ne["lat"], clamp_lng(ne["lng"])],
        ]
        st.session_state.markers.append(
            {
                'coords': [lat, lng],
                'boundingbox': bbox,
                'zoom': st_data['zoom']
            }
        )
        st.rerun()

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
