import streamlit as st
from app.translations import results


def mape_evaluation():
    if mape >= .15:
        text = results['mape_eval_high'][lang].format(mape=mape*100)
        return text
    elif mape >= .10:
        text = results['mape_eval_avg'][lang].format(mape=mape*100)
        return text
    else:
        text = results['mape_eval_low'][lang].format(mape=mape*100)
        return text


def go_home():
    st.session_state.go_home = True


if 'go_home' in st.session_state:
    del st.session_state.go_home
    del st.session_state.lang
    st.switch_page('main.py')

st.set_page_config(
    page_title="Results",
    page_icon="📊",
    initial_sidebar_state='collapsed'
)

lang = st.session_state['lang']

try:
    mape = round(st.session_state['prediction']['value']['mape'], 2)
    value = round(st.session_state['prediction']['value']['property_price'], 2)
    model = st.session_state['prediction']['model']

    min_val, max_val = value * (1-mape), value * (1+mape)
    percent = (mape - min_val) / (max_val - min_val) * 100

except:
    a, b = st.columns(2, vertical_alignment='center')
    with a:
        st.markdown(results['error'][lang])
        st.button(
            results['home_button'][lang],
            icon='🏠',
            type="primary",
            on_click=go_home
            )
    with b:
        st.image("https://cdn-icons-png.flaticon.com/512/9068/9068699.png")
    
    st.markdown("---")
    st.html(
        '<a href="https://www.flaticon.com/free-icons/close" title="close icons">Close icons created by Fathema Khanom - Flaticon</a>'
    )
    st.stop()

st.title(results['evaluation'][lang].format(value=value))
# f":green[$ {value:,.0f}]."

st.markdown(results['range_text'][lang])

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
{results['range_limit_min'][lang]}
                
## :red[$ {min_val:,.0f}]""")
with col2:
    st.markdown(f"""
{results['range_limit_avg'][lang]}
                
## :green[$ {value:,.0f}]""")

with col3:
    st.markdown(f"""
{results['range_limit_max'][lang]}

## :blue[$ {max_val:,.0f}]""")

st.markdown(f"""---""")
st.title(results['about_estimator_title'][lang])

st.markdown(
    results['about_estimator_text'][lang]
        .format(mape_evaluation=mape_evaluation()))

st.markdown(f"""---""")

st.title(results['about_creators_title'][lang])

st.markdown(results['about_creators_Marcus_text'][lang])

st.markdown(results['about_creators_model'][lang]
    .format(author=model.model['author']))

if model.model['links']:
    text_links = []
    for item, link in model.model['links'].items():
        text_links.append(f"[{item}]({link})")
    st.markdown(" | ".join(text_links))

st.markdown('---')
st.button(
    results['home_button'][lang],
    icon='🏠',
    type="primary",
    on_click=go_home,
    use_container_width=True
)