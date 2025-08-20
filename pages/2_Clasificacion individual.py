import streamlit as st
import pandas as pd
import joblib 
import os
import time


mapeo_tamainak = {
    '< 2M €': '< 2M €',
    '2M - 10M €': '2M - 10M €',
    '10M - 50M €': '10M - 50M €',
    '> 50M €': ' > 50M €'
}

@st.cache_data
def asignar_temperatura(puntuacion):
    if puntuacion >=92:
        return "🔥🔥 Caliente"
    elif puntuacion >= 86:
        return "🔥 Caliente"
    elif puntuacion >= 82:
        return "🌡️ Templado"
    else:
        return "❄️ Frío"

mapeo_provincias = {
            'araba': 'Álava',
            'cantabria': 'Cantabria',
            'gipuzkoa': 'Guipúzcoa',
            'huesca': 'Huesca',
            'la rioja': 'La Rioja',
            'nafarroa': 'Navarra',
            'bizkaia': 'Vizcaya',
            'zaragoza': 'Zaragoza'
        }

mapeo_provincias_reverso = {v: k for k, v in mapeo_provincias.items()}

df = pd.read_csv('dataframe.csv', sep=';')
df['sector'] = df['sektore_propioa']
df['contratando'] = df['dolor_leve'] + df['dolor_agudo']
df['contratando'] = df['contratando'].apply(lambda x: 'Sí' if x > 0 else 'No')
df['menciones_prensa'] = df['notizia'].apply(lambda x: 'Sí' if x > 0 else 'No')
df['tamaño'] = df['tamaño_facturacion'].map(mapeo_tamainak)
df['facturación'] = df['tamaño_facturacion']
df['empleados'] = df['tamaño_empleados']
df['provincia '] = df['provincia'].map(mapeo_provincias)



st.subheader("Introduce los datos para clasificar el Lead:")

st.write("""Introduce los datos de la empresa que quieras analizar de forma manual.  
El modelo evaluará la información y devolverá una calificación: **frío, templado o caliente**.  
Además, añadirá una breve explicación con las señales que justifican esa clasificación, para que entiendas de un vistazo por qué la empresa se ubica en esa categoría.
""")

col1, col2, col3 = st.columns(3)


facturacion = col1.selectbox("Facturacion (en millones de euros)", ['< 2M €', '2M - 10M €', '10M - 50M €', '> 50M €'])
empleados = col2.selectbox("Empleados", ['1 - 10', '11 - 50', '51 - 200', '201 - 500', '> 500'])
sector = col3.selectbox("Sector", ['comercio', 'industria', 'infraestructuras', 'logistica', 'servicios', 'tecnologia', 'otros/desconocido'])
provincia = col1.selectbox("Provincia", list(mapeo_provincias.values()))
contratando = col2.selectbox("Contratando", ["Sí", "No"],index=1) 
menciones_en_prensa = col3.selectbox("Menciones en Prensa", ["Sí", "No"], index=1)
nombre_empresa = 'test'

provincia2 = mapeo_provincias_reverso[provincia]


if contratando == "Sí":
    dolor_agudo = 1
else:
    dolor_agudo = 0
dolor_leve = 0

if menciones_en_prensa == "Sí":
    notizia = 1
else:
    notizia = 0

datuak = [[nombre_empresa ,facturacion, empleados, sector, provincia2, dolor_leve, dolor_agudo, notizia]]

df = pd.DataFrame(datuak, columns=["nombre_de_la_empresa", "tamaño_facturacion", "tamaño_empleados", "sektore_propioa", "provincia", "dolor_leve", "dolor_agudo", "notizia"])


modeloa =joblib.load('pipeline_modelo_final_v1.0.pkl')
y_pred = modeloa.predict(df)

calculo_lead = col2.button("Clasificar Lead individual")

temperatura = asignar_temperatura(y_pred[0])

negativo, positivo, neutral = False, False, False

if calculo_lead:
    haserako_unea = time.time()
    y_pred = modeloa.predict(df)
    temperatura = asignar_temperatura(y_pred[0])
    bukaerako_unea = time.time()

    kalkulurako_denbora = bukaerako_unea - haserako_unea

    st.success(f"¡Clasificación completada! {len(df)} lead procesado y puntuado en {kalkulurako_denbora*1000:.4f} milisegundos.")


    

    if temperatura == "❄️ Frío":
        negativo = True
    elif temperatura == "🌡️ Templado":
        neutral = True
    else:
        positivo = True

    if facturacion == '< 2M €':
        if empleados in ['51 - 200', '201 - 500', '> 500']:
            texto = 'porque se trata de una microempresa con una base trabajadora grande para las ventas que produce'
        else:
            texto = 'porque se trata de una microempresa'      
    elif facturacion == '2M - 10M €':
        if empleados == '1 - 10':
            texto = 'porque se trata de una empresa pequeña con unas ventas muy interesantes para la base de trabajadores que tiene'
        elif empleados in ['11 - 50', '51 - 200']:
            texto = 'porque se trata de una empresa pequeña'
        elif empleados in ['201 - 500', '> 500']:
            texto = 'porque se trata de una empresa pequeña con una base trabajadora demasiado grande para las ventas que produce'
    elif facturacion == '10M - 50M €':
        if empleados == '1 - 10':
            texto = 'porque se trata de una empresa mediana con unas ventas muy interesantes para la base de trabajadores que tiene'
        elif empleados in ['11 - 50', '51 - 200', '201 - 500']:
            texto = 'porque se trata de una empresa mediana'
        elif empleados == '> 500':
            texto = 'porque se trata de una empresa mediana con una base trabajadora demasiado grande para las ventas que produce'
    elif facturacion == '> 50M €':
            texto = 'porque se trata de una empresa grande'


    if sector == 'industria':
        texto2 = 'en el sector industrial, que es el sector mas caliente, con diferencia, en estos momentos.'
    elif sector == 'comercio':
        texto2 = 'en el sector comercial, que es un sector bastante interesante en estos momentos.'
    elif sector in ['infraestructuras', 'tecnologia']:
        texto2 = f'en el sector {sector}, que es un sector menos interesante en estos momentos.'
    else:
        texto2 = f'en el sector {sector}, que es un sector poco interesante en estos momentos.'

    if positivo is True:
        if contratando == 'Sí':
            if menciones_en_prensa == 'Sí':
                texto3 = ' Ademas, estan contratando, y tiene menciones en prensa.'
            else:
                texto3 = ' Ademas, estan contratando.'
        else:
            if menciones_en_prensa == 'Sí':
                texto3 = ' Ademas, tiene menciones en prensa.'
            else:
                texto3 = ' Es una empresa que no esta contratando, ni tiene menciones en prensa.'

    if negativo is True:
        if contratando == 'Sí':
            if menciones_en_prensa == 'Sí':
                texto3 = ' Pero, estan contratando, y tiene menciones en prensa.'
            else:
                texto3 = ' Aun asi, estan contratando.'
        else:
            if menciones_en_prensa == 'Sí':
                texto3 = ' De todas formas, sí que obtiene menciones en prensa.'
            else:
                texto3 = 'Ademas, es una empresa que no genera noticias relacionadas con la innovación, ni esta contratando.'

    if neutral is True:
        if contratando == 'Sí':
            if menciones_en_prensa == 'Sí':
                texto3 = ' Pero, estan contratando, y tiene menciones en prensa.'
            else:
                texto3 = ' Aun asi, estan contratando.'
        else:
            if menciones_en_prensa == 'Sí':
                texto3 = ' De todas formas, tiene menciones en prensa.'
            else:
                texto3 = ' Y es una empresa que no genera noticias relacionadas con la innovación, ni esta contratando.'


    if negativo:
        texto4 = 'Hasta que mejoren las cosas, de momento, mejor no tocar.'
    elif positivo:
        if temperatura == '🔥🔥 Caliente':
            texto4 = 'Deja lo que estes haciendo y llamales.'
        else:
            texto4 = "Ponte en contacto en cuanto puedas."
    else:
        texto4 = 'De momento , mantenles el ojo encima.'

    
    st.write(f"Este lead es {temperatura}  {texto} {texto2} {texto3} {texto4}")






    # st.write("Tu lead es caliente (85/100) porque es una empresa mediana (+15), del sector industrial (+10) y está contratando (+30).... Transparencia total. Confianza instantánea.")

    st.markdown("---")

   
