"""Aplicación Streamlit del sistema difuso académico."""

import streamlit as st

from ui.pages import PAGES, disclaimer
from ui.design import install_design, brand, hero

st.set_page_config(page_title="Sistema difuso académico", page_icon="❤️", layout="wide", initial_sidebar_state="expanded")

# La aplicación ya está en español. Esta marca evita que la traducción automática
# de Chrome modifique el DOM administrado por React y provoque errores removeChild.
st.markdown('<meta name="google" content="notranslate">', unsafe_allow_html=True)

install_design()

if "weight_input" not in st.session_state:
    st.session_state.weight_input = 75.0
if "age_input" not in st.session_state:
    st.session_state.age_input = 50
if "result" not in st.session_state:
    st.session_state.result = None

with st.sidebar:
    brand()
hero()
disclaimer()

page_name = st.sidebar.radio("Navegación", list(PAGES))
st.sidebar.caption("SEMINARIO IA\n\nLaboratorio de lógica difusa\n\nUso exclusivamente académico")
PAGES[page_name]()
