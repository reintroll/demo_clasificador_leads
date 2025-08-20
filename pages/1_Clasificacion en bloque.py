import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import os
import joblib 
import time
import requests
from matplotlib.ticker import MaxNLocator

  
uploaded_file = None

df = None # Inicializa df a None

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
    
mapeo_tamainak = {
    '< 2M €': '< 2M €',
    '2M - 10M €': '2M - 10M €',
    '10M - 50M €': '10M - 50M €',
    '> 50M €': ' > 50M €'
}

mapeo_provincias = {
            'araba': 'Álava',
            'bizkaia': 'Vizcaya',
            'gipuzkoa': 'Guipúzcoa',
            'nafarroa': 'Navarra',
            'la rioja': 'La Rioja',
            'cantabria': 'Cantabria',
            'huesca': 'Huesca',
            'zaragoza': 'Zaragoza'
        }

# GeoJSON
geojson_url = "https://gist.github.com/josemamira/3af52a4698d42b3f676fbc23f807a605/raw/provincias_spain.geojson"
geojson = requests.get(geojson_url).json()

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("Archivo CSV cargado exitosamente.")
    except Exception as e:
        st.error(f"Error al cargar el archivo CSV: {e}")
        st.info("Asegúrate de que el archivo es un CSV válido y está bien formateado.")
else:

    df = pd.read_csv('dataframe.csv', sep=';')
    df['sector'] = df['sektore_propioa']
    df['contratando'] = df['dolor_leve'] + df['dolor_agudo']
    df['contratando'] = df['contratando'].apply(lambda x: 'Sí' if x > 0 else 'No')
    df['menciones_prensa'] = df['notizia'].apply(lambda x: 'Sí' if x > 0 else 'No')
    df['tamaño'] = df['tamaño_facturacion'].map(mapeo_tamainak)
    df['facturación'] = df['tamaño_facturacion']
    df['empleados'] = df['tamaño_empleados']
    df['provincia '] = df['provincia'].map(mapeo_provincias)

    df = df.sample(frac=1, random_state=42).reset_index(drop=True)


if df is not None:
    st.subheader("Vista Previa de los Datos de Leads")
   

    # Mostrar las primeras filas por defecto, con opción de ver todo
    mostrar_todo = st.checkbox("Mostrar todos los datos", value=False)

    if mostrar_todo:
        st.write(f"Mostrando {len(df)} filas y {len(df.columns)} columnas.")
        st.write("""
        Aquí tienes una muestra de datos reales de empresas.  

        Al pulsar el botón **“Clasificar Leads”**, el modelo procesará toda la lista y asignará a cada empresa una etiqueta: **frío, templado o caliente**.  
        Después, generará un análisis general con las tendencias más relevantes, para que veas al instante dónde están las oportunidades y cómo se mueve el mercado.

         """)
        st.dataframe(df[['nombre_de_la_empresa','facturación', 'empleados', 'sector', 'provincia ', 'contratando', 'menciones_prensa']], use_container_width=True) # use_container_width hace que ocupe todo el ancho disponible
    else:
        st.write(f"Mostrando las primeras {min(10, len(df))} filas de {len(df)}.")
        st.write("""
        Aquí tienes una muestra de datos reales de empresas.  

        Al pulsar el botón **“Clasificar Leads”**, el modelo procesará toda la lista y asignará a cada empresa una etiqueta: **frío, templado o caliente**.  
        Después, generará un análisis general con las tendencias más relevantes, para que veas al instante dónde están las oportunidades y cómo se mueve el mercado.

         """)
        st.dataframe(df[['nombre_de_la_empresa','facturación', 'empleados', 'sector', 'provincia ', 'contratando', 'menciones_prensa']].head(10), use_container_width=True)

    with st.expander("Analisis preliminar de la cartera.", expanded=False):
        col1, col2  = st.columns(2)
        col1.text("Leads por Sector")
        col1.bar_chart(df['sector'].value_counts(), horizontal=True, stack='layered', height=400, color='#346daf')
        col2.text("Leads por Tamaño")
        col2.bar_chart(df['tamaño'].value_counts(), horizontal=True, height=400, color='#346daf')
    
    col1, col2  = st.columns([2,3])

    clasificar = col2.button("Clasificar Leads")
    if clasificar:
        haserako_unea = time.time()
        st.markdown("---")
        st.subheader("Clasificación en bloque de los Datos de Leads")
       
        # cargar modelo de clasificacion

        path_modeloa = os.path.join( '..', '04_models', 'final', 'pipeline_modelo_final_v1.0.pkl')
        
        modeloa =joblib.load(path_modeloa)
        df_pred = df.copy()

        y_pred = modeloa.predict(df_pred)
        
        df_pred['label'] = y_pred
        df_pred['temperatura'] = df_pred['label'].apply(asignar_temperatura)

        bukaerako_unea = time.time()

        kalkulurako_denbora = bukaerako_unea - haserako_unea

        st.success(f"¡Clasificación completada! {len(df_pred)} leads procesados y puntuados en {kalkulurako_denbora:.2f} segundos.")

        st.dataframe(df_pred[['nombre_de_la_empresa', 'facturación', 'empleados', 'sector', 'provincia ', 'contratando', 'menciones_prensa', 'temperatura']], use_container_width=True) # use_container_width hace que ocupe todo el ancho disponible
        st.markdown("---")

        st.subheader("Analisis de Leads")

        col1, col2, col3 = st.columns(3)

        col1.metric("🔥 Leads Calientes", len(df_pred[df_pred['label'] >= 86]))
        col2.metric("🌡️ Leads Templados", len(df_pred[(df_pred['label'] >= 82) & (df_pred['label'] < 86)]))
        col3.metric("❄️ Leads Frios", len(df_pred[df_pred['label'] < 82]))


        st.markdown("---")

        # nos quedamos solo con los temperatura = caliente
        df_calientes = df_pred[df_pred['label'] >= 86] 

        
        col1, col2  = st.columns(2)

        ## graf sektoreka

        col1.text("Leads Calientes por Sector")

        col1.bar_chart(df_calientes['sector'].value_counts(), horizontal=True, stack='layered', height=400, color='#346daf')


        ## graf tamainaz

        col2.text("Leads Calientes por Facturación")
       
        col2.bar_chart(df_calientes['tamaño'].value_counts(), horizontal=True, height=400, color='#346daf')


        ## graf probintziak

        # Agrupar por provincia y contar menciones

        df_calientes['provincia2'] = df_calientes['provincia']
        
        df_localidad = df_calientes.groupby('provincia2').agg(
            count=('provincia2', 'count'),
            suma_temperatura=('label', 'sum')
        ).reset_index() ### df_calientes erabili leads calientes bakarrik ikusteko. df_pred erabili 100 lead-ak ikusteko

        df_localidad['promedio_temperatura'] = df_localidad['suma_temperatura'] / df_localidad['count']
        df_localidad = df_localidad.rename(columns={'count': 'leads'})

        
        # probintzia izenak zuzen grafikorako
        df_localidad['provincia'] = df_localidad['provincia2'].map(mapeo_provincias)



        fig = px.choropleth(df_localidad,
                            geojson=geojson,
                            locations="provincia",
                            featureidkey="properties.Texto",  # cambia si el campo de nombre es otro
                            color="leads",
                            color_continuous_scale="Blues",
                            hover_data=[],
                            scope="europe")

        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(coloraxis_showscale=True, title = 'Leads Calientes por Provincias')
        fig.update_layout(coloraxis_colorbar = dict(title = 'temperatura', tickvals = []))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',  # fondo transparente fuera del gráfico
            plot_bgcolor='rgba(0,0,0,0)'    # fondo transparente dentro del gráfico
        )

        col1.plotly_chart(fig)


        col2.subheader("Inteligencia Clave Detectada")

        muy_calientes = df_pred[df_pred['label'] >= 92]
        sector_top = df_pred['sector'].value_counts().index[0]
        ayudas = df_pred[df_pred['notizia'] > 0]
        porcentaje_medianas = len(df_calientes[df_calientes['tamaño'] == '10M - 50M €']) / len(df_calientes)
        porcentaje_pequeñas = len(df_calientes[df_calientes['tamaño'] == '2M - 10M €']) / len(df_calientes)
        porcentaje_pymes = round((porcentaje_medianas + porcentaje_pequeñas)*100)


        col2.write(f'🎯  Oportunidad de Élite: En total hemos detectado {len(muy_calientes)} leads muy calientes. Estas empresas no solo contratan, sino que buscan puestos estratégicos (Directivos, Ingenieros Senior). Estas representan las oportunidades de mayor valor.')
        col2.write(f'📈 Tendencia de Sector: El sector {sector_top} es el que muestra una mayor actividad de contratación de alto nivel en este momento.')
        col2.write(f'💡 Señal de Innovación: {len(ayudas)} empresas de esta lista han recibido ayudas o menciones en prensa relacionadas con la innovación en los últimos 2 anos.')
        col2.write(f'🏭 Pulso Pyme: Un {porcentaje_pymes}% de las compañías identificadas como calientes son pequeñas y medianas empresas, lo que indica un terreno fértil para relaciones más directas, ciclos de decisión más cortos y mayor agilidad en la adopción de soluciones.')

        st.markdown("---")