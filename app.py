import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import geopandas as gpd


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
.highlight-box {{
    border: 1px solid {BORDER_COLOR};
    padding: 10px;
    border-radius: 10px;
    background-color: {BG_COLOR};
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
<div class="highlight-box">
<p style="margin: 0;">Nombre d'observations (séismes) : <span style="font-weight: bold; color: {TEXT_COLOR};">3 272 774</span> / Nombre de variables: <span style="font-weight: bold; color: {TEXT_COLOR};">22</span></p>
</div>
''', unsafe_allow_html=True)

st.divider()

st.subheader("Informations sur le dataset")

# Afficher le début du parquet
with st.expander("Exemple de données"):
    st.write("Extrait des données brutes (CSV) :")
    df_lite = pd.read_csv('data/earthquakes_lite.csv')
    st.dataframe(df_lite.tail(5), hide_index=True)
    st.markdown(f'''
    <div class="highlight-box">
    <p>Le nettoyage se fait sur :</p>
    <ul>
    <li>Les colonnes nst et magNst contiennent à la fois des 0 et des valeurs vides (NaN). Or dans ce dataset, 0 ne signifie pas 0 station, mais plutôt “information non fournie”, exactement comme NaN. Cette ambiguïté rend la colonne peu fiable et source de confusion, donc nous convertissons ces valeurs en NaN.</li>
    <li>Vérification valeurs faussement différentes dans "place" (ex : central East Pacific Rise, Central East Pacific Rise) pour les regrouper sous une même appellation à des fins d'analyse cohérente.</li>
    </ul>
    </div>
    ''', unsafe_allow_html=True)
    st.write("")
    st.write("Extrait des données après conversion des types et nettoyage (Parquet) :")
    df_converted = pd.read_parquet('data/earthquakes_lite.parquet')
    st.dataframe(df_converted.tail(5), hide_index=True)

# Afficher les significations des variables
with st.expander("Significations des variables et types (après conversion du csv vers parquet)"):
    df_significations = pd.DataFrame([
    ['date', 'datetime64', 'Moment exact du séisme. Souvent au format ISO 8601 (ex : 2025-02-03T14:32:12.345Z). UTC.'],
    ['latitude', 'Float64', 'Coordonnées géographiques de l’épicentre du séisme. latitude : Nord/Sud'],
    ['longitude', 'Float64', 'Coordonnées géographiques de l’épicentre du séisme. longitude : Est/Ouest'],
    ['profondeur_km', 'Float64', 'Profondeur de l’hypocentre du séisme sous la surface terrestre. En kilomètres.'],
    ['magnitude', 'Float64', 'Magnitude du séisme (taille/énergie).'],
    ['type_magnitude', 'string', 'Type de magnitude utilisée : - Mw : magnitude de moment (la plus fiable) - ML : magnitude locale (Richter) - Mb : ondes de volume - Md : durée etc.'],
    ['nb_stations_localisation', 'Int64', 'Nombre de stations sismiques utilisées pour calculer la localisation du séisme.'],
    ['ecart_azimut', 'Float64', 'Angle "gap" en degrés : → indique la couverture par les stations autour de l’épicentre. → plus c’est bas, meilleure est la localisation du séisme.'],
    ['distance_min', 'Float64', 'Distance horizontale minimale entre l’épicentre et la station la plus proche. En degrés (coordonnées), pas en km.'],
    ['rms', 'Float64', 'Résidu moyen (Root Mean Square) du modèle de localisation. Plus c’est faible, plus la localisation est précise.'],
    ['reseau', 'string', 'Code du réseau sismique qui a reporté l’événement. (ex : us, ak, nc, etc.)'],
    ['ID', 'string', 'Identifiant unique du séisme dans la base de données.'],
    ['date_maj_infos', 'datetime64', 'Date de la dernière mise à jour de l’événement (par ex. corrections apportées après analyses).'],
    ['lieu', 'string', 'Description textuelle de la localisation. Ex : "10 km NE of Los Angeles, California"'],
    ['type', 'string', 'Type d’événement : - earthquake - quarry blast - explosion - ice quake etc.'],
    ['erreur_horiz', 'Float64', 'Incertitude horizontale (latitude/longitude) en km.'],
    ['erreur_profondeur', 'Float64', 'Incertitude sur la profondeur (en km).'],
    ['erreur_magnitude', 'Float64', 'Incertitude sur la magnitude.'],
    ['nb_stations_magnitude', 'Int64', 'Nombre de stations utilisées spécifiquement pour calculer la magnitude.'],
    ['mag_uniforme', 'Float64', 'Magnitude normalisée pour faciliter les comparaisons entre différents types de magnitude.'],
], columns=['Colonne', 'Type', 'Signification'])
    st.dataframe(df_significations, hide_index=True, height=200)


with st.expander("Quelques observations sur les données après nettoyage et conversion des types"):
    st.markdown(f'''
                
    <!-- Observation -->    
    <div class="observation-box">
    <p style="margin: 0;">Les variables suivantes ont des valeurs manquantes : ID (<span style="font-weight: bold; color: {TEXT_COLOR};">0</span>), date (<span style="font-weight: bold; color: {TEXT_COLOR};">0</span>), lieu (<span style="font-weight: bold; color: {TEXT_COLOR};">11</span>), magnitude (<span style="font-weight: bold; color: {TEXT_COLOR};">155 698</span>), type_magnitude (<span style="font-weight: bold; color: {TEXT_COLOR};">166 609</span>), latitude (<span style="font-weight: bold; color: {TEXT_COLOR};">0</span>), longitude (<span style="font-weight: bold; color: {TEXT_COLOR};">0</span>), profondeur_km (<span style="font-weight: bold; color: {TEXT_COLOR};">9</span>), mag_uniforme (<span style="font-weight: bold; color: {TEXT_COLOR};">701 438</span>), nb_stations_localisation (<span style="font-weight: bold; color: {TEXT_COLOR};">1 204 826</span>), nb_stations_magnitude (<span style="font-weight: bold; color: {TEXT_COLOR};">1 091 476</span>), ecart_azimut (<span style="font-weight: bold; color: {TEXT_COLOR};">834 294</span>), rms (<span style="font-weight: bold; color: {TEXT_COLOR};">210 659</span>), erreur_horiz (<span style="font-weight: bold; color: {TEXT_COLOR};">1 524 519</span>), erreur_profondeur (<span style="font-weight: bold; color: {TEXT_COLOR};">603 806</span>), erreur_magnitude (<span style="font-weight: bold; color: {TEXT_COLOR};">1 772 000</span>), type (<span style="font-weight: bold; color: {TEXT_COLOR};">0</span>), date_maj_infos (<span style="font-weight: bold; color: {TEXT_COLOR};">0</span>).</p>
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

st.subheader("Cartes des tremblements de terre")
with open('earthquake_map.html', 'r') as f:
    html_content = f.read()
components.html(html_content, height=600)

st.divider()

st.subheader("Statistiques descriptives")

# # Diviser la page en 3 colonnes
# col1, col2, col3 = st.columns(3)

# with col1:
#     # Charger les données avec mag_uniform
#     df_uniform = pd.read_parquet('data/STEP04_earthquakes.parquet')
#     df_uniform = df_uniform.dropna(subset=['mag_uniform'])  # Supprimer les NaN

#     # Calculer les statistiques
#     stats = df_uniform['mag_uniform'].describe()
#     q1 = stats['25%']
#     median = stats['50%']
#     q3 = stats['75%']
#     min_val = stats['min']
#     max_val = stats['max']
#     mean_val = stats['mean']

#     # Créer le boxplot pour mag_uniform (horizontal)
#     fig2, ax2 = plt.subplots()
#     ax2.boxplot(df_uniform['mag_uniform'], vert=False)
#     ax2.set_title('Boxplot des magnitudes uniformisées')
#     ax2.set_xlabel('Magnitude uniformisée')
#     st.pyplot(fig2)

#     st.markdown(f'''
                
#     <!-- Observation -->
#     <div class="observation-box">
#     <p style="margin: 0;">Statistiques des magnitudes uniformisées : Min = {min_val:.2f}, Q1 = {q1:.2f}, Médiane = {median:.2f}, Moyenne = {mean_val:.2f}, Q3 = {q3:.2f}, Max = {max_val:.2f}.</p>
#     </div>

#     ''', unsafe_allow_html=True)

# with col2:
#     # Charger les données pour les statistiques
#     df_stats = pd.read_parquet('data/STEP04_earthquakes.parquet')
#     df_stats = df_stats.dropna(subset=['magType'])  # Supprimer les NaN dans magType

#     # Compter les occurrences de chaque type de magnitude en pourcentage
#     magtype_counts = df_stats['magType'].value_counts(normalize=True) * 100

#     # Grouper les valeurs < 3% dans "Others"
#     others = magtype_counts[magtype_counts < 3].sum()
#     magtype_counts = magtype_counts[magtype_counts >= 3]
#     if others > 0:
#         magtype_counts['Others'] = others

#     # Créer un graphique en barres
#     fig, ax = plt.subplots()
#     magtype_counts.plot(kind='bar', ax=ax)
#     ax.set_title('Pourcentage d\'utilisations par type de magnitude')
#     ax.set_xlabel('Type de magnitude')
#     ax.set_ylabel('Pourcentage (%)')
#     plt.xticks(rotation=45)
#     st.pyplot(fig)

#     st.markdown(f'''
                
#     <!-- Observation -->
#     <div class="observation-box">
#     <p style="margin: 0;">On voit de multiples types de magnitude utilisés, ce qui peut compliquer l'analyse directe sans conversion uniforme. D'où la nouvelle colonne 'mag_uniform'.</p>
#     </div>

#     ''', unsafe_allow_html=True)

# with col3:
#     # Charger les données pour la carte des continents
#     df_map = pd.read_parquet('data/STEP04_earthquakes.parquet')
#     df_map = df_map.dropna(subset=['latitude', 'longitude'])

#     # Créer un GeoDataFrame pour les points
#     gdf_points = gpd.GeoDataFrame(df_map, geometry=gpd.points_from_xy(df_map.longitude, df_map.latitude), crs='EPSG:4326')

#     # Charger la carte du monde
#     url = "others/ne_110m_admin_0_countries.zip"
#     world = gpd.read_file(url)

#     # Joindre spatialement pour obtenir le continent
#     joined = gpd.sjoin(gdf_points, world, how='left', predicate='within')

#     # Compter les tremblements par continent
#     continent_counts = joined['CONTINENT'].value_counts()

#     # Ajouter les counts à la carte du monde
#     world['earthquake_count'] = world['CONTINENT'].map(continent_counts).fillna(0)

#     # Tracer la carte choroplèthe
#     fig3, ax3 = plt.subplots(1, 1, figsize=(10, 6))
#     world.plot(column='earthquake_count', ax=ax3, legend=True, cmap='Reds', edgecolor='black')
#     ax3.set_title('Nombre de tremblements de terre par continent')
#     ax3.set_axis_off()
#     st.pyplot(fig3)
