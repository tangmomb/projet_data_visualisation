import streamlit as st
import pandas as pd


# Couleurs pour l'interface
BORDER_COLOR = "#3b558d"
BG_COLOR = "#101e3c"
TEXT_COLOR = "#63d2ff"
BORDER_COLOR_LITE = "#474747"

# Styles CSS personnalisés
st.markdown(f"""
<style>
.observation-box {{
    border: 1px solid {BORDER_COLOR_LITE};
    padding: 15px;
    border-radius: 10px;
    background-color: transparent;
    margin-bottom: 15px;
}}
ul {{
    margin-top: 0;
    margin-bottom: 0;
    padding-left: 20px;
}}
li {{
    margin: 10px 0;
}}
</style>
""", unsafe_allow_html=True)

st.set_page_config(layout="wide")

st.title("Tremblements de terre (1970 - 2019)")

st.write("Tremblements de terre enregistrés dans le monde entier de 1970 à mars 2019. Les données proviennent de l'USGS (United States Geological Survey) et incluent des informations telles que la magnitude, la localisation, la profondeur, la date et l'heure des tremblements de terre.")

st.markdown(f'''
<a href="https://www.kaggle.com/datasets/danielpe/earthquakes" target="_blank">
<button style="background-color: #1e2629; border: none; color: white; padding: 5px 10px; text-align: center; text-decoration: none; display: inline-block; font-size: 12px; margin: 4px 2px; cursor: pointer; border-radius: 4px;">
<img src="https://www.kaggle.com/static/images/site-logo.svg" alt="Kaggle" style="height: 16px; vertical-align: middle; margin-right: 5px;">
Dataset Kaggle
</button>
</a>
''', unsafe_allow_html=True)

# Afficher la forme
st.markdown(f'''
<div style="    
    border: 1px solid {BORDER_COLOR};
    padding: 10px;
    border-radius: 10px;
    background-color: {BG_COLOR};">
<p style="margin: 0;">Nombre d'observations (séismes) : <span style="font-weight: bold; color: {TEXT_COLOR};">3 272 774</span> / Nombre de variables: <span style="font-weight: bold; color: {TEXT_COLOR};">22</span></p>
</div>
''', unsafe_allow_html=True)

st.divider()

st.subheader("Informations sur le dataset")

# Afficher le début du parquet
with st.expander("Exemple de données"):
    st.write("Extrait des données brutes (CSV) :")
    df_lite = pd.read_csv('csv/earthquakes_lite.csv')
    st.dataframe(df_lite.tail(5), hide_index=True)
    st.write("Le nettoyage se fait sur :")
    st.markdown("- La colonne nst contient à la fois des 0 et des valeurs vides (NaN). Or dans ce dataset, 0 ne signifie pas 0 station, mais plutôt “information non fournie”, exactement comme NaN. Cette ambiguïté rend la colonne peu fiable et source de confusion, donc il est préférable de la supprimer.")
    st.write("Extrait des données après conversion des types et nettoyage (Parquet) :")
    df_converted = pd.read_parquet('csv/earthquakes_lite.parquet')
    st.dataframe(df_converted.tail(5), hide_index=True)

# Afficher les significations des variables
with st.expander("Significations des variables et types (après conversion)"):
    df_significations = pd.DataFrame([
        ['time', 'datetime64', 'Moment exact du séisme. Souvent au format ISO 8601 (ex : 2025-02-03T14:32:12.345Z). UTC.'],
        ['latitude', 'Float64', 'Coordonnées géographiques de l’épicentre du séisme. latitude : Nord/Sud'],
        ['longitude', 'Float64', 'Coordonnées géographiques de l’épicentre du séisme. longitude : Est/Ouest'],
        ['depth', 'Float64', 'Profondeur de l’hypocentre du séisme sous la surface terrestre. En kilomètres.'],
        ['mag', 'Float64', 'Magnitude du séisme (taille/énergie).'],
        ['magType', 'string', 'Type de magnitude utilisée : - Mw : magnitude de moment (la plus fiable) - ML : magnitude locale (Richter) - Mb : ondes de volume - Md : durée etc.'],
        ['nst', 'Int64', 'Nombre de stations sismiques utilisées pour calculer la localisation du séisme.'],
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
    st.dataframe(df_significations, hide_index=True, height=200)


with st.expander("Quelques observations sur les données brutes"):
    st.markdown(f'''
                
    <!-- Observation -->    
    <div class="observation-box">
    <p style="margin: 0;">Les variables suivantes ont des valeurs manquantes : depth (<span style="font-weight: bold; color: {TEXT_COLOR};">9</span>), mag (<span style="font-weight: bold; color: {TEXT_COLOR};">156449</span>), magType (<span style="font-weight: bold; color: {TEXT_COLOR};">167407</span>), nst (<span style="font-weight: bold; color: {TEXT_COLOR};">881566</span>), gap (<span style="font-weight: bold; color: {TEXT_COLOR};">838549</span>), dmin (<span style="font-weight: bold; color: {TEXT_COLOR};">1346742</span>), rms (<span style="font-weight: bold; color: {TEXT_COLOR};">211653</span>), place (<span style="font-weight: bold; color: {TEXT_COLOR};">11</span>), horizontalError (<span style="font-weight: bold; color: {TEXT_COLOR};">1531963</span>), depthError (<span style="font-weight: bold; color: {TEXT_COLOR};">606685</span>), magError (<span style="font-weight: bold; color: {TEXT_COLOR};">1781012</span>), magNst (<span style="font-weight: bold; color: {TEXT_COLOR};">988917</span>), status (<span style="font-weight: bold; color: {TEXT_COLOR};">1</span>).</p>
    </div>

    ''', unsafe_allow_html=True)

    # Charger le contenu du fichier Markdown
    with open('valeurs_manquantes.md', 'r', encoding='utf-8') as f:
        md_content = f.read()
        with st.popover("Voir pourquoi"):
            st.markdown(md_content)

    st.markdown(f'''
                
    <!-- Observation -->
    <div class="observation-box">
    <p style="margin: 0;">Certaines villes ou lieux apparaissent plusieurs fois mais les coordonnées peuvent varier pour plus de précision. Voir l'exemple de Washington ci-dessus.</p>
    </div>

    ''', unsafe_allow_html=True)


st.divider()

st.subheader("Statistiques descriptives")