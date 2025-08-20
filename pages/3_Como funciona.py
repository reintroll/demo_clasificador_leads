import streamlit as st
import pandas as pd
import altair as alt


st.subheader("Nuestra Metodología: Transparencia y Resultados")

st.text("Nuestro sistema no es una caja negra mágica. Es un motor de análisis que hemos entrenado para operar con la misma lógica que usan los estrategas para ganar. Funciona en dos pasos: primero, recopila y procesa miles de datos públicos sobre las empresas; segundo, un modelo de inteligencia artificial analiza esos datos para identificar los patrones que indican un alto potencial de crecimiento, basándose en lo que ha funcionado en el mundo real.")


st.subheader('¿En qué se fija nuestro modelo?')



tamaño_empleados = 0.012381979790097365
tamaño_facturacion = 0.013507665872281766
sektore_propioa = 0.003969115232580626
provincia = 0.011070537081721192
notizia = 0.02972929369367627
dolor_leve = 0.01134020963303313
dolor_agudo = 0.026340380923807362


señales_de_crecimiento_activo = dolor_leve + dolor_agudo # contratacion
perfil_de_la_empresa = tamaño_empleados + tamaño_facturacion + sektore_propioa
visibilidad_en_el_mercado = notizia

datos = {
    "variable": [
        "señales_de_crecimiento_activo",
        "perfil_de_la_empresa",
        "visibilidad_en_el_mercado"
    ],
    "valor": [
        dolor_leve + dolor_agudo,
        tamaño_empleados + tamaño_facturacion,
        notizia
    ]
}

df = pd.DataFrame(datos)
df["variable"] = df["variable"].str.replace("_", " ")


chart = alt.Chart(df).mark_bar(color="#346daf").encode(
    x="valor:Q",
    y=alt.Y("variable:N", sort="-x", axis=alt.Axis(title=None, labelLimit=400)),  # Orden descendente por valor
    tooltip=["variable", "valor"]      # Para ver valores al pasar el ratón
).properties(
    width=600,
    height=300
)

st.altair_chart(chart, use_container_width=True)

st.text('Nuestro modelo da máxima importancia a las señales de acción: lo que una empresa hace. Las contrataciones (crecimiento activo) y las menciones en prensa (visibilidad en el mercado) pesan más que los datos demográficos como plantilla, facturación o sector. Creemos que el comportamiento reciente es el mejor indicador del potencial futuro.')
st.subheader("¿Cómo de fiable es nuestro sistema?")

st.text( """Sometemos nuestro modelo a pruebas rigurosas para garantizar que no solo es potente, sino también consistente. Piense en nuestro sistema como un tirador de élite.
Puntería (R² Score): 0.81
¿Qué significa? Esta métrica nos dice la precisión con la que nuestro sistema apunta. Un 0.81 significa que es capaz de explicar el 81% del potencial de un lead, acertando consistentemente muy cerca del centro de la diana.
Consistencia (RMSE): 3.3 puntos
¿Qué significa? Esta métrica mide la agrupación de los disparos. En una escala de 0 a 100, nuestras predicciones suelen tener una desviación media de solo 3.3 puntos. Esto garantiza que no solo apuntamos bien, sino que nuestros resultados son fiables y predecibles.""")

st.subheader('¿Quieres saber más?')
st.write("""Lo que ha visto es una demostración. Una fotografía de las oportunidades que existen en su mercado.
Pero la verdadera pregunta no es qué puede hacer esta herramienta con 100 empresas de ejemplo.
La verdadera pregunta es: ¿Qué podría hacer por usted con los datos de sus propios clientes potenciales?
Imagine tener esta claridad, no una vez, sino cada semana. Imagine a su equipo comercial empezando cada lunes con una lista priorizada de los leads con más probabilidades de cerrar, sabiendo exactamente por qué deben contactarlos primero.
Si lo que ha visto le resulta interesante, el siguiente paso es simple.         
         
         """)

col1, col2, col3 = st.columns([3,5,1])

URL_FORMULARIO_TALLY = 'https://tally.so/r/mBygA7'

col2.markdown(
    f"""
    <a href="{URL_FORMULARIO_TALLY}" target="_blank">
        <button style="
            font-weight: bold;
            padding: 0.75rem 1.5rem;
            border-radius: 0.5rem;
            background-color: #346daf;
            color: white;
            border: none;
            cursor: pointer;
        ">
            Solicitar mi "Diagnóstico de Potencial" Gratuito
        </button>
    </a>
    """,
    unsafe_allow_html=True
)
col1, col2, col3 = st.columns([2,7,1])
col2.caption("Una sesión de 30 minutos, sin compromiso, donde analizaremos cómo aplicar esta metodología a sus desafíos específicos.")


