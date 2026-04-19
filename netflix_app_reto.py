import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account
import json

key_dict = json.loads(st.secrets['textkey'])
creds = service_account.Credentials.from_service_account_info(key_dict)

db = firestore.Client(credentials=creds, project='movies-dec74')
dbMovies = db.collection('movies')
                         
movies_ref = list(db.collection(u'movies').stream())
movies_dict = list(map(lambda x: x.to_dict(), movies_ref))
movies_dataframe = pd.DataFrame(movies_dict)
#st.dataframe(movies_dataframe)

# Título de la app
st.title('Netflix App')

# Barra lateral
sidebar = st.sidebar
sidebar.title('Mostrar todos los filmes')
# checkbox
st.header('Filmes')
agree = sidebar.checkbox('Mostrar todos los filmes recuperados')
if agree:
    st.dataframe(movies_dataframe)

# buscar por titulo
def load_data_bytitulo(tit):
    data = movies_dataframe[movies_dataframe['name'].str.contains(tit, case=False)]
    return data
titulo = sidebar.text_input('Título de la película: ')
boton = sidebar.button('Buscar título')
if (boton):
    filterbytitulo = load_data_bytitulo(titulo)
    st.dataframe(filterbytitulo)

# seleccionar director
def load_data_bydir(dir):
    data = movies_dataframe[movies_dataframe['director']==dir]
    return data
select_dir = sidebar.selectbox('Select director', movies_dataframe['director'].unique())
boton2 = sidebar.button('Filtrar director')
if (boton2):
    filterbydir = load_data_bydir(select_dir)
    st.dataframe(filterbydir)

# insertar filme
with st.sidebar.form("my_form"):
    st.subheader('Insertar filme')
    titulo2 = st.text_input('Título de la película: ')
    director = st.text_input('Director: ')
    genero = st.text_input('Género: ')
    company = st.text_input('Compañía: ')
    boton3 = st.form_submit_button('Agregar filme')

if boton3:
    nueva_peli = {
        'name': titulo2,
        'genre': genero,
        'director': director,
        'company': company
    }

    db.collection('movies').add(nueva_peli)
    st.success("Película agregada correctamente 🎬")

    docs = db.collection('movies').stream()
    data = []
    for doc in docs:
        data.append(doc.to_dict())
    nuevo_movies = pd.DataFrame(data)
    st.dataframe(nuevo_movies)