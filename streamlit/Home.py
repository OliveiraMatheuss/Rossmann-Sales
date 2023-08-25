import streamlit.components.v1 as components
import streamlit as st
from PIL import Image
from  app import main


st.set_page_config(
    page_title="Rossmann",
    page_icon="🧊",
    layout="wide")

with st.sidebar:
            components.html("""
                            <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="large" data-theme="light" data-type="VERTICAL" data-vanity="oliveiramatheuss" data-version="v1"><a class="badge-base__link LI-simple-link" href="https://br.linkedin.com/in/oliveiramatheuss?trk=profile-badge"></a></div>
                            <script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>              
                    """, height= 310)

image = Image.open('img/Rossmann.png')


st.image(image, width = 400)

st.subheader('Você pode escolher entre intervalos de identificação das lojas usando a aba Slider ou selecionar lojas individualmente pela aba Multiselect.')

main()
