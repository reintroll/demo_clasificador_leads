import streamlit as st
import pandas as pd
import os
import joblib # Necesario para cargar el modelo
import io # Necesario para el botón de descarga

# --- Configuración de la página de Streamlit ---
st.set_page_config(
    page_title="Demo Clasificador de Leads",
    page_icon="📊",
    layout="wide" # Usa un layout amplio para mejor visualización
)

st.title("📊 Demo: Clasificador de Leads")


st.warning("Esta demo usa datos de ejemplo. Usa la barra lateral para filtrar y explorar los datos.")
st.warning("No se proporcionan datos reales de clientes.")
st.error("""falta zuzentzeko:\n
           empleados eta facturacion numerikoak izango dira, eta filtroan rangoka\n
           contratando eta mencion ez dira 0/1 izango si/no baizik bisualki\n
           columnen izenburuak ere erabakitzeko
           """)
st.write("Esta aplicación demuestra la visualización de datos de leads para un clasificador.")

# --- Cargar el archivo CSV ---
# Puedes subir un archivo CSV directamente o usar uno predefinido para la demo.
# Para la demo, es útil tener un archivo de ejemplo para que funcione al instante.

# Opción 1: Subida de archivo por el usuario
uploaded_file = st.file_uploader("Sube tu archivo CSV de leads", type=["csv"])

df = None # Inicializa df a None

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("Archivo CSV cargado exitosamente.")
    except Exception as e:
        st.error(f"Error al cargar el archivo CSV: {e}")
        st.info("Asegúrate de que el archivo es un CSV válido y está bien formateado.")
else:
    # Opción 2: Usar un archivo de ejemplo si no se sube ninguno
    st.info("No se ha subido ningún archivo. Se mostrarán datos de ejemplo.")
    # Crea un DataFrame de ejemplo para la demo
    ruta_csv = os.path.join(os.path.dirname(__file__), '..', '01_data', 'raw', 'leads_muestreo.csv')
    df = pd.read_csv(ruta_csv)
    df = df.drop('puntuacion', axis=1)


if df is not None:
    # --- filtros ---
    st.sidebar.header("Filtros")

    # Filtro por localidad
    localidad_filtro = st.sidebar.selectbox("Localidad", ["Todos"] + list(df["localidad"].unique()))
    if localidad_filtro != "Todos":
        df = df[df["localidad"] == localidad_filtro]

    # Filtro por sector
    sector_filtro = st.sidebar.selectbox("Sector", ["Todos"] + list(df["sector"].unique()))
    if sector_filtro != "Todos":
        df = df[df["sector"] == sector_filtro]

    # Filtro por empleados

    # gehitu script haseran esateko zein den langile gehieneko enpresa, top bezala erabiltzeko
    # blokeka erabiltzeko jarri sliderra

    empleados_filtro = st.sidebar.selectbox("Empleados", ["Todos"] + list(df["empleados"].unique()))
    if empleados_filtro != "Todos":
        df = df[df["num_empleados_rango"] == empleados_filtro]

    empleados_filtro2 = st.sidebar.slider("Rango de empleados", value=(0, 100))
    # df = df[(df["empleados"] >= empleados_filtro2[0]) & (df["empleados"] <= empleados_filtro2[1])]

    # Filtro por antigüedad

    # gehitu script haseran esateko zein den aintzinatasun altueneko enpresa, top bezala erabiltzeko
    # blokeka erabiltzeko jarri sliderra

    antiguedad_filtro = st.sidebar.selectbox("Antiguedad", ["Todos"] + list(df["antiguedad"].unique()))
    if antiguedad_filtro != "Todos":
        df = df[df["antiguedad"] == antiguedad_filtro]


    # Filtro por facturación

    # gehitu script haseran esateko zein den aintzinatasun altueneko enpresa, top bezala erabiltzeko
    # blokeka erabiltzeko jarri sliderra

    facturacion_filtro = st.sidebar.selectbox("Facturación", ["Todos"] + list(df["facturacion"].unique()))
    if facturacion_filtro != "Todos":
        df = df[df["facturacion"] == facturacion_filtro]

    # Filtro por contratando
    contratando_filtro = st.sidebar.selectbox("Contratando", ["Todos"] + list(df["contratando"].unique()))
    if contratando_filtro != "Todos":
        df = df[df["contratando"] == contratando_filtro]

    # Filtro por mención en prensa
    mencion_prensa_filtro = st.sidebar.selectbox("Mención en Prensa", ["Todos"] + list(df["mencion"].unique()))
    if mencion_prensa_filtro != "Todos":
        df = df[df["mencion"] == mencion_prensa_filtro]

    # Filtro por puntuación
    # puntuacion_filtro = st.sidebar.selectbox("Puntuación", ["Todos"] + list(df["puntuacion"].unique()))
    # if puntuacion_filtro != "Todos":
    #     df = df[df["puntuacion"] == puntuacion_filtro]

    st.subheader("Vista Previa de los Datos de Leads")

    # Mostrar las primeras filas por defecto, con opción de ver todo
    mostrar_todo = st.checkbox("Mostrar todos los datos (puede ser lento para datasets grandes)", value=False)

    if mostrar_todo:
        st.write(f"Mostrando {len(df)} filas y {len(df.columns)} columnas.")
        st.dataframe(df, use_container_width=True) # use_container_width hace que ocupe todo el ancho disponible
    else:
        st.write(f"Mostrando las primeras {min(10, len(df))} filas de {len(df)}.")
        st.dataframe(df.head(10), use_container_width=True)

    st.markdown("---")

    # --- Visualización de Datos Categoricos ---
    st.subheader("Visualización de Datos Categoricos")



    # Sector con mas Leads
 
    sector_max = df['sector'].value_counts().idxmax()
    conteo = df['sector'].value_counts()[sector_max]
    st.metric("El sector con mayor cantidad de leads es:", sector_max + " (" + str(conteo) + ")")



    col1, col2, col3 = st.columns(3)


    # cantidad frio/caliente
    conteo = df.groupby("empleados").size().reset_index(name="conteo")
    col1.text("Conteo por empleados")
    col1.write (df['empleados'].value_counts())



    # conteo por facturacion
    conteo = df.groupby("facturacion").size().reset_index(name="conteo")
    col2.text("Conteo por facturacion")
    col2.write(df['facturacion'].value_counts())


    # conteo por antiguedad
    df['antiguo'] = pd.cut(df['antiguedad'], bins=[0, 5, 10, 25, 100], labels=['≤5', '6-10', '11-25', '>26'])
    col3.text("Conteo por antiguedad")
    col3.write(df["antiguo"].value_counts())


    st.markdown("---")

    # --- Botón de Descarga (Opcional pero útil para la demo) ---
    @st.cache_data # Cachea la función para evitar recalcular el CSV cada vez
    def convert_df_to_csv(dataframe):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return dataframe.to_csv(index=False).encode('utf-8')


    # --- Espacio para el clasificador (futuro) ---
    st.subheader("Clasificador de Leads")
    clasificar = st.button("Clasificar Leads")
    if clasificar:
       
        # cargar modelo de clasificacion

        modeloa = joblib.load('../04_models/checkpoints/random_forest_model_v01.pkl')
        df_inf = df.copy()
        df_inf = df_inf.drop('antiguo', axis=1)

        # inferencia 


        y_pred = modeloa.predict(df_inf)
        df_inf['puntuacion'] = y_pred

        # mostrar_todo_inf = st.checkbox("Mostrar todos los datos", value=False)


        st.write(f"Mostrando {len(df_inf)} filas y {len(df_inf.columns)} columnas.")
        st.dataframe(df_inf, use_container_width=True) # use_container_width hace que ocupe todo el ancho disponible



        csv_download = convert_df_to_csv(df_inf)

        st.download_button(
            label="Descargar Datos CSV",
            data=csv_download,
            file_name="datos_leads.csv",
            mime="text/csv",
            help="Haz clic para descargar los datos mostrados en formato CSV."
        )

    
    st.markdown("---")

    st.subheader("Clasificador de Leads in-line")

    st.text("Introduce tus propios datos para calcular la puntuación del Lead:")

    col1, col2, col3, col4 = st.columns(4)

    nombre_empresa = col1.text_input("Nombre de la Empresa")
    localidad = col1.selectbox("Localidad", list(df["localidad"].unique()))
    sector = col2.selectbox("Sector", list(df["sector"].unique()))
    empleados = col2.selectbox("Empleados", list(df["empleados"].unique()))
    facturacion = col3.selectbox("Facturacion", list(df["facturacion"].unique()))
    antiguedad = col3.text_input("Antiguedad")
    contratando = col4.selectbox("Contratando", ["Si", "No"]) 
    if contratando == "Si":
        contratando = 1
    else:
        contratando = 0
    menciones_en_prensa = col4.selectbox("Menciones en Prensa", ["Si", "No"])
    if menciones_en_prensa == "Si":
        menciones_en_prensa = 1
    else:
        menciones_en_prensa = 0

    calculo_lead = st.button("Clasificar Lead in-line")

    if calculo_lead:
        df_inline = pd.DataFrame([[nombre_empresa, localidad, sector, empleados, facturacion, antiguedad, contratando, menciones_en_prensa]], columns=["nombre_empresa", "localidad", "sector", "empleados", "facturacion", "antiguedad", "contratando", "mencion"])
       
        # cargar modelo de clasificacion

        modeloa = joblib.load('../04_models/checkpoints/random_forest_model_v01.pkl')
        y_pred = modeloa.predict(df_inline)
        st.write(f"La puntuación del Lead es: {y_pred[0]}")






else:
    st.warning("Por favor, sube un archivo CSV o espera a que se carguen los datos de ejemplo.")



st.markdown("---")
