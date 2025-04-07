import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
print(os.getcwd())

# Directorio donde están los archivos CSV
csv_directory = 'wikiSpider/data_lake/consumption_zone/'
# df = pd.read_csv('wikiSpider/data_lake/consumption_zone/=_newsmergepider__2025-04-06.csv')

# Lista para almacenar los DataFrames
df_list = []

# Iterar sobre todos los archivos en la carpeta
for file in os.listdir(csv_directory):
    # Verificar si el archivo tiene extensión .csv
    if file.endswith('.csv'):
        # Crear la ruta completa del archivo
        file_path = os.path.join(csv_directory, file)
        
        # Leer el archivo CSV y agregarlo a la lista de DataFrames
        df = pd.read_csv(file_path)
        df_list.append(df)

# Combinar todos los DataFrames en uno solo
df = pd.concat(df_list, ignore_index=True)

# Mostrar el DataFrame combinado
print("asdf")
print(df)
print("asdf")
@st.cache_resource  # cachea la conexión para eficiencia
def get_connection():
    # information Connection with db
    hostname = os.getenv('DB_HOST')
    username = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    database = os.getenv('DB_DATABASE')
    
    return psycopg2.connect(
            host=hostname,
            user=username,
            password=password,
            dbname=database
        )

# Función general para ejecutar una query y devolver resultados como DataFrame
def run_query(sql_query, params=None):
    conn = get_connection()
    with conn.cursor() as cursor:
        if params:
            cursor.execute(sql_query, params)
        else:
            cursor.execute(sql_query)
        colnames = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=colnames)
    return df

# Consultar todos los artículos
def get_all_articles():
    query = "SELECT * FROM news ORDER BY date DESC;"
    return run_query(query)

def get_count_articles():
    query = "select count(*) from news;"
    return run_query(query)

raw_curr = requests.get('https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/bob.json')
if raw_curr.status_code == 200:
    raw = dict(raw_curr.json())
curr = '' 

if 'bob' in raw and '1inch' in raw['bob']:
    curr = (raw['bob']['1inch'])

response = requests.get('https://timeapi.io/api/timezone/zone?timeZone=America%2FLa_Paz')
if response.status_code == 200:
    tz_data = response.json()
    current_time = tz_data['currentLocalTime']
    time_zone = tz_data['timeZone']
    formatted_date = datetime.fromisoformat(current_time).strftime("%d/%m/%Y")
    formatted_time = datetime.fromisoformat(current_time).strftime("%H:%M:%S")
else:
    formatted_time = ''
    time_zone = ''
    formatted_date = ''

with st.container(border=True):
        st.image('./informatica.png', use_container_width=True)

with st.container(border=True):
    col1, col2 = st.columns([1,4], vertical_alignment='center', gap='small')
    # col1, col2 = st.columns(2, vertical_alignment='center', gap='small')

    with col1:
        st.metric(label='Currency Boliviano', value=curr, delta=0.05)
        st.success(f"Hora actual en {time_zone}:")
        st.markdown(f"🕒 {formatted_time}")
        st.markdown(f"{formatted_date}")
        # st.text('columna1')
    with col2:
        queryDb = get_count_articles()
        st.html(
        f"<h1 style='text-align: center; font-size: 35px;'> News Dashboard con Streamlit</h1>"
        f"<h4 style='text-align: center;'>Total Scraped {queryDb.iloc[0,0]}</h4>"
        )
    
col3, col4 = st.columns(2, vertical_alignment='top', gap='medium')

with col3:

    # Conteo de artículos por tag
    tag_count = df['tag'].value_counts()

    # Mostrar el conteo como texto
    st.write("### Conteo de Artículos por Tag")
    st.write(tag_count)

    # Mostrar el gráfico de barras
    st.bar_chart(tag_count)

    st.divider()

    df['body_length'] = df['body'].apply(len)
    df['intro_length'] = df['intro'].apply(len)

    st.write("### Resumen de Longitudes de Cuerpo e Introducción")
    st.write("Longitud Promedio del Cuerpo de los Artículos:", df['body_length'].mean())
    st.write("Longitud Promedio de la Introducción:", df['intro_length'].mean())

    # Mostrar las estadísticas descriptivas
    st.write(df[['body_length', 'intro_length']].describe())

with col4:
    tag_rate = df.groupby(['date', 'tag']).size().unstack().fillna(0)

    # Calcular la tasa de crecimiento diaria por tag
    tag_rate_daily = tag_rate.diff().fillna(0)

    st.write("### Tasa de Publicación de Artículos por Tag")
    st.line_chart(tag_rate_daily)
    
    st.divider()
    
    url_distribution = df['url'].value_counts()

    # Gráfico de barras de la distribución de artículos por URL
    st.write("### Distribución de Artículos por URL")
    st.bar_chart(url_distribution)
