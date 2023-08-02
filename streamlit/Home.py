from  app import main
from description import description
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Rossmann",
    page_icon="🧊",
    layout="wide")

image = Image.open('img/Rossmann.png')

st.image(image, width = 400)

tab1, tab2 = st.tabs([':dart: Descrição','📈Previsão'])

with tab1:
    description()

with tab2:
    main()
