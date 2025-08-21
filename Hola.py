import streamlit as st

#hide github icon
hide_github_icon = """

.css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
"""
st.markdown(hide_github_icon, unsafe_allow_html=True)

st.set_page_config(
    page_title="Demo Clasificador de Leads",
    page_icon="🎯",
    layout="wide"
)

st.write("Bienvenido a la Demo Clasificador de Leads")



st.markdown("""
            ## Introducción  

Esta aplicación es una **demo interactiva** para explorar cómo un clasificador de leads puede transformar datos en **decisiones estratégicas**.  
Aquí no solo ves números: ves **prioridades, señales y oportunidades**.  

👈 Usa la barra lateral para navegar entre los distintos modos de uso.  

---

## Clasificación en bloque  

Ejemplo **real y aplicable**: carga un archivo con leads y obtén una clasificación masiva.  
En segundos verás **qué empresas destacan, qué señales activan el radar y dónde conviene enfocar recursos**.  

---

## Clasificación unitaria  

Cuando necesitas analizar un lead en particular: introduce los datos manualmente y obtén su **valor estratégico individual**.  
Ideal para validar hipótesis concretas o comparar un lead específico frente al resto.  

---

## Cómo funciona  

En esta sección abrimos la “caja negra” del modelo:  
- Qué variables considera para puntuar un lead  
- Cómo pondera cada señal  
- Y qué tan **fiables** son sus predicciones  

Así puedes entender no solo el resultado, sino también la **lógica que lo respalda**.  

""")
