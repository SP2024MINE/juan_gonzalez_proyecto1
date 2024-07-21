import streamlit as st
from sodapy import Socrata
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from dotenv import load_dotenv
load_dotenv('../.env')


st.title('Covid contagios')
st.write('Mi primer aplicativo para contagios covid')



TOKEN_APP = os.getenv("SECRET_TOKEN")
TOKEN_USER = os.getenv("TOKEN_USER")
TOKEN_PASS = os.getenv("TOKE_PASS")

client = Socrata(
        "www.datos.gov.co",
        TOKEN_APP,
        username= TOKEN_USER,
        password= TOKEN_PASS,
        timeout=5000)


consulta =  """SELECT fecha_de_notificaci_n, id_de_caso, departamento_nom, edad, sexo, estado, 
recuperado, fecha_inicio_sintomas, fecha_muerte, fecha_recuperado
limit 1000"""
data_id = "gt2j-8ykr"

results = client.get(data_id, query = consulta)
df = pd.DataFrame.from_records(results)


caso = st.selectbox('Seleccion un caso', df['id_de_caso'], placeholder= 'Seleccione un caso unico')

dataset_caso = df[df['id_de_caso'] == caso].T
st.dataframe(dataset_caso)

##visualizacion de contagios por departamento
st.write('Visualizacion de contratos por departamento')
df['departamento_nom'] = df['departamento_nom'].str.upper()

#usamos sns para visualizar los contratos por departamento
fig, ax = plt.subplots()
sns.countplot(data= df, x = 'departamento_nom', ax = ax)
plt.xticks(rotation = 90)
st.pyplot(fig)