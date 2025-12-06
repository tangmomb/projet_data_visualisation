import streamlit as st
import pandas as pd


st.set_page_config(layout="wide")

st.title("Tremblements de terre (1970 - 2019)")

st.write("Tremblements de terre enregistrés dans le monde entier de 1970 à mars 2019. Les données proviennent de l'USGS (United States Geological Survey) et incluent des informations telles que la magnitude, la localisation, la profondeur, la date et l'heure des tremblements de terre.")
st.markdown("[Lien vers le dataset](https://www.kaggle.com/datasets/danielpe/earthquakes)")

# Afficher la forme
st.markdown('''
<div style="    
    border: 1px solid #283144;
    padding: 10px;
    border-radius: 10px;
    background-color: #10151f;">
<h3>Forme du dataset</h3>
<p>Nombre d'observations (séismes) : 3272774 / Nombre de variables: 22</p>
</div>
''', unsafe_allow_html=True)


# Afficher les significations des variables
st.subheader("Significations des variables et types (après conversion)")
df_significations = pd.DataFrame([
    ['time', 'datetime64', 'Moment exact du séisme. Souvent au format ISO 8601 (ex : 2025-02-03T14:32:12.345Z). UTC.'],
    ['latitude', 'Float64', 'Coordonnées géographiques de l’épicentre du séisme. latitude : Nord/Sud'],
    ['longitude', 'Float64', 'Coordonnées géographiques de l’épicentre du séisme. longitude : Est/Ouest'],
    ['depth', 'Float64', 'Profondeur de l’hypocentre du séisme sous la surface terrestre. En kilomètres.'],
    ['mag', 'Float64', 'Magnitude du séisme (taille/énergie). Forme non précisée ici : peut être ML, Mw, Mb...'],
    ['magType', 'string', 'Type de magnitude utilisée : - Mw : magnitude de moment (la plus fiable) - ML : magnitude locale (Richter) - Mb : ondes de volume - Md : durée etc.'],
    ['nst', 'Int64', 'Nombre de stations sismiques ayant détecté le séisme.'],
    ['gap', 'Float64', 'Angle "gap" en degrés : → indique la couverture par les stations autour de l’épicentre. → plus c’est bas, meilleure est la localisation du séisme.'],
    ['dmin', 'Float64', 'Distance horizontale minimale entre l’épicentre et la station la plus proche. En degrés (coordonnées), pas en km.'],
    ['rms', 'Float64', 'Résidu moyen (Root Mean Square) du modèle de localisation. Plus c’est faible, plus la localisation est précise.'],
    ['net', 'string', 'Code du réseau sismique qui a reporté l’événement. (ex : us, ak, nc, etc.)'],
    ['id', 'string', 'Identifiant unique du séisme dans la base de données.'],
    ['updated', 'datetime64', 'Date de la dernière mise à jour de l’événement (par ex. corrections apportées après analyses).'],
    ['place', 'string', 'Description textuelle de la localisation. Ex : "10 km NE of Los Angeles, California"'],
    ['type', 'string', 'Type d’événement : - earthquake - quarry blast - explosion - ice quake etc.'],
    ['horizontalError', 'Float64', 'Incertitude horizontale (latitude/longitude) en km.'],
    ['depthError', 'Float64', 'Incertitude sur la profondeur (en km).'],
    ['magError', 'Float64', 'Incertitude sur la magnitude.'],
    ['magNst', 'Int64', 'Nombre de stations utilisées spécifiquement pour calculer la magnitude.'],
    ['status', 'string', 'Statut du séisme : - automatic : détermination automatique, non révisée - reviewed : contrôlé par un sismologue'],
    ['locationSource', 'string', 'Réseau qui a fourni la localisation.'],
    ['magSource', 'string', 'Réseau qui a fourni la magnitude.']
], columns=['Colonne', 'Type', 'Signification'])
st.dataframe(df_significations, hide_index=True)

# Afficher le début du CSV
st.subheader("Début du dataset")
df_lite = pd.read_csv('csv/earthquakes_lite.csv')
st.dataframe(df_lite, hide_index=True)



