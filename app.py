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

st.title("Tremblements de terre aux USA  de 2000 à 2005")

st.write("le dataset original traite des tremblements de terre dans le monde entier entre 1970 et mars 2019. Nous le travaillons pour nous concentrer sur les tremblements de terre enregistrés aux USA de 2000 à 2005 et avoir un nombre d'observations plus raisonnable. Les données proviennent de l'USGS (United States Geological Survey).")

st.markdown(f'''
<a href="https://www.kaggle.com/datasets/danielpe/earthquakes" target="_blank">
<button style="background-color: #1e2629; border: none; color: white; padding: 5px 10px; text-align: center; text-decoration: none; display: inline-block; font-size: 12px; margin: 4px 2px; cursor: pointer; border-radius: 4px;">
<img src="https://www.kaggle.com/static/images/site-logo.svg" alt="Kaggle" style="height: 16px; vertical-align: middle; margin-right: 5px;">
Dataset Kaggle
</button>
</a>
''', unsafe_allow_html=True)

# Calculer le nombre d'observations et de variables à partir du CSV
df_shape = pd.read_csv('data/earthquakes.csv', nrows=0)
with open('data/earthquakes.csv', 'r', encoding='utf-8') as f:
    n_obs = sum(1 for _ in f) - 1  # -1 pour l'en-tête
n_vars = len(df_shape.columns)

# Calculer et afficher la forme (brut + nettoyage) dans une seule balise
df_parquet = pd.read_parquet('data\STEP11_earthquakes.parquet')
n_obs_parquet = len(df_parquet)
n_vars_parquet = len(df_parquet.columns)
st.markdown(f'''
<div class="highlight-box">
<p style="margin: 0;">Nombre d'observations sur dataset brut (séismes) : <span style="font-weight: bold; color: {TEXT_COLOR};">{n_obs:,}</span> / Nombre de variables: <span style="font-weight: bold; color: {TEXT_COLOR};">{n_vars}</span></p>
<p style="margin: 0;">Nombre d'observations après nettoyage : <span style="font-weight: bold; color: {TEXT_COLOR};">{n_obs_parquet:,}</span> / Nombre de variables: <span style="font-weight: bold; color: {TEXT_COLOR};">{n_vars_parquet}</span></p>
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
    <li>Conversion des types de données (dates, numériques) et sauvegarde en Parquet pour une meilleure performance.</li>
    <li>Suppression des doublons strictement identiques et des doublons sur l'ID unique.</li>
    <li>Les colonnes nst et magNst contiennent à la fois des 0 et des valeurs vides (NaN). Or dans ce dataset, 0 ne signifie pas 0 station, mais plutôt "information non fournie", exactement comme NaN. Cette ambiguïté rend la colonne peu fiable et source de confusion, donc nous convertissons ces valeurs en NaN.</li>
    <li>Vérification valeurs faussement différentes dans "place" (ex : central East Pacific Rise, Central East Pacific Rise) pour les regrouper sous une même appellation à des fins d'analyse cohérente, en normalisant les textes (suppression accents, ponctuation, espaces).</li>
    <li>Ajout d'une colonne 'mag_uniforme' pour normaliser les magnitudes selon leur type (Mw, ML, etc.) afin de faciliter les comparaisons. On calcule une magnitude uniforme approximative mais réaliste à des fins statistiques. Certains types de magnitude ne se prêtent pas à cette normalisation d'où les valeurs manquantes parfois.</li>
    <li>Suppression des colonnes que nous n'utiliserons pas : 'net', 'locationSource', 'magSource', 'status', 'dmin'. Le dataset est déjà suffisamment dense.</li>
    <li>Réorganisation des colonnes et renommage en français pour une meilleure lisibilité.</li>
    <li>Suppression des évènements autres que "earthquake" et suppression de la colonne "type"</li>
    <li>Filtrage spatial pour ne garder que les séismes aux USA et dans un rayon de 50 km autour, de 2000 à 2005.</li>
    <li>Ajout d'une colonne "ressenti" indiquant si le séisme est probablement ressenti par l'humain selon des critères de magnitude et profondeur.</li>
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
        ['ID', 'string', 'Identifiant unique du séisme dans la base de données.'],
        ['date', 'datetime64', 'Moment exact du séisme. Souvent au format ISO 8601 (ex : 2025-02-03T14:32:12.345Z). UTC.'],
        ['lieu', 'string', 'Description textuelle de la localisation. Ex : "10 km NE of Los Angeles, California"'],
        ['magnitude', 'Float64', 'Magnitude du séisme (taille/énergie).'],
        ['type_magnitude', 'string', 'Type de magnitude utilisée.'],
        ['latitude', 'Float64', 'Coordonnées géographiques de l’épicentre du séisme. latitude : Nord/Sud'],
        ['longitude', 'Float64', 'Coordonnées géographiques de l’épicentre du séisme. longitude : Est/Ouest'],
        ['profondeur_km', 'Float64', 'Profondeur de l’hypocentre du séisme sous la surface terrestre. En kilomètres.'],
        ['mag_uniforme', 'Float64', 'Magnitude normalisée pour faciliter les comparaisons entre différents types de magnitude.'],
        ['nb_stations_localisation', 'Int64', 'Nombre de stations sismiques utilisées pour calculer la localisation du séisme.'],
        ['nb_stations_magnitude', 'Int64', 'Nombre de stations utilisées spécifiquement pour calculer la magnitude.'],
        ['ecart_azimut', 'Float64', 'Indique la couverture par les stations autour de l’épicentre. Plus c’est bas, meilleure est la localisation du séisme.'],
        ['rms', 'Float64', 'Résidu moyen (Root Mean Square) du modèle de localisation. Plus c’est faible, plus la localisation est précise.'],
        ['erreur_horiz', 'Float64', 'Incertitude horizontale (latitude/longitude) en km.'],
        ['erreur_profondeur', 'Float64', 'Incertitude sur la profondeur (en km).'],
        ['erreur_magnitude', 'Float64', 'Incertitude sur la magnitude.'],
        ['ressenti', 'string', 'Indique si le séisme est probablement ressenti par l’humain selon des critères de magnitude et profondeur.'],
        ['date_maj_infos', 'datetime64', 'Date de la dernière mise à jour de l’événement (par ex. corrections apportées après analyses).'],
    ], columns=['Colonne', 'Type', 'Signification'])
    st.dataframe(df_significations, hide_index=True, height=200)


with st.expander("Quelques observations sur les données après nettoyage et conversion des types"):
    df_full = pd.read_parquet('data/STEP11_earthquakes.parquet')
    missing_values = df_full.isnull().sum()
    columns = ['ID', 'date', 'lieu', 'magnitude', 'type_magnitude', 'latitude', 'longitude', 'profondeur_km', 'mag_uniforme', 'nb_stations_localisation', 'nb_stations_magnitude', 'ecart_azimut', 'rms', 'erreur_horiz', 'erreur_profondeur', 'erreur_magnitude', 'ressenti', 'date_maj_infos']
    missing_formatted = [f"{col} (<span style=\"font-weight: bold; color: {TEXT_COLOR};\">{missing_values[col]:,}</span>)".replace(",", " ") for col in columns if missing_values[col] > 0]
    missing_text = ", ".join(missing_formatted)
    st.markdown(f'''
                
    <!-- Observation -->    
    <div class="observation-box">
    <p style="margin: 0;">Les variables suivantes ont des valeurs manquantes : {missing_text}.</p>
    </div>

    ''', unsafe_allow_html=True)

    # Charger le contenu du fichier Markdown
    with open('assets/valeurs_manquantes.md', 'r', encoding='utf-8') as f:
        md_content = f.read()
        with st.popover("Voir pourquoi"):
            st.markdown(md_content)

    st.markdown(f'''
                
    <!-- Observation -->
    <div class="observation-box">
    <p style="margin: 0;">Certaines villes ou lieux apparaissent plusieurs fois mais les coordonnées peuvent varier pour plus de précision. Voir l'exemple du Nevada ci-dessus.</p>
    </div>

    ''', unsafe_allow_html=True)

st.divider()

st.subheader("Densité des tremblements de terre aux USA de 2000 à 2005")
with open('assets/earthquake_map_areas.html', 'r') as f:
    html_content = f.read()
components.html(html_content, height=600)

st.divider()

st.subheader("Statistiques descriptives")

# Diviser la page en 3 colonnes
col1, col2, col3 = st.columns(3)

with col1:
    # Charger les données avec mag_uniform
    df_uniform = pd.read_parquet('data/STEP11_earthquakes.parquet')
    df_uniform = df_uniform.dropna(subset=['mag_uniforme'])  # Supprimer les NaN

    # Calculer les statistiques
    stats = df_uniform['mag_uniforme'].describe()
    q1 = stats['25%']
    median = stats['50%']
    q3 = stats['75%']
    min_val = stats['min']
    max_val = stats['max']
    mean_val = stats['mean']

    # Créer le boxplot pour mag_uniforme (horizontal)
    fig2, ax2 = plt.subplots()
    ax2.boxplot(df_uniform['mag_uniforme'], vert=False)
    ax2.set_title('Boxplot des magnitudes uniformisées')
    ax2.set_xlabel('Magnitude uniformisée')
    st.pyplot(fig2)

    st.markdown(f'''
                
    <!-- Observation -->
    <div class="observation-box">
    <p style="margin: 0;">Statistiques des magnitudes uniformisées : Min = {min_val:.2f}, Q1 = {q1:.2f}, Médiane = {median:.2f}, Moyenne = {mean_val:.2f}, Q3 = {q3:.2f}, Max = {max_val:.2f}.</p>
    </div>

    ''', unsafe_allow_html=True)

with col2:
    # Charger les données pour les statistiques
    df_stats = pd.read_parquet('data/STEP11_earthquakes.parquet')
    df_stats = df_stats.dropna(subset=['type_magnitude'])  # Supprimer les NaN dans magType

    # Compter les occurrences de chaque type de magnitude en pourcentage
    magtype_counts = df_stats['type_magnitude'].value_counts(normalize=True) * 100

    # Grouper les valeurs < 3% dans "Others"
    others = magtype_counts[magtype_counts < 3].sum()
    magtype_counts = magtype_counts[magtype_counts >= 3]
    if others > 0:
        magtype_counts['Others'] = others

    # Créer un graphique en barres
    fig, ax = plt.subplots()
    magtype_counts.plot(kind='bar', ax=ax)
    ax.set_title('Pourcentage d\'utilisations par type de magnitude')
    ax.set_xlabel('Type de magnitude')
    ax.set_ylabel('Pourcentage (%)')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.markdown(f'''
                
    <!-- Observation -->
    <div class="observation-box">
    <p style="margin: 0;">On voit de multiples types de magnitude utilisés, ce qui peut compliquer l'analyse directe sans conversion uniforme. D'où la nouvelle colonne 'mag_uniform'.</p>
    </div>

    ''', unsafe_allow_html=True)

with col3:
    # Charger les données pour la répartition des magnitudes uniformisées
    df_uniform = pd.read_parquet('data/STEP11_earthquakes.parquet')
    df_uniform = df_uniform.dropna(subset=['mag_uniforme'])  # Supprimer les NaN
    bins = [-float('inf'), 1, 2, 3, 4, float('inf')]
    labels = ['<1', '1-2', '2-3', '3-4', '>4']
    mag_uniforme_bins = pd.cut(df_uniform['mag_uniforme'], bins=bins, labels=labels)
    proportions = mag_uniforme_bins.value_counts(normalize=True).sort_index() * 100
    counts = mag_uniforme_bins.value_counts().sort_index()

    fig, ax1 = plt.subplots()
    color = 'tab:blue'
    ax1.set_xlabel('Magnitude uniformisée')
    ax1.set_ylabel('Nombre', color=color)
    bars = ax1.bar(labels, counts, color=color, alpha=0.6, label='Nombre')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim(0, 235000)  # Limite de l'axe y

    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax1.annotate(f'{int(height)}\n{proportions.iloc[i]:.1f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom', color='black', fontsize=10, fontweight='bold')

    ax1.set_title("Répartition des magnitudes uniformisées")
    fig.tight_layout()
    st.pyplot(fig)

    st.markdown(f'''
                
    <!-- Observation -->
    <div class="observation-box">
    <p style="margin: 0;">La majorité des séismes sont de faible magnitude (< 2).</p>
    </div>

    ''', unsafe_allow_html=True)


# --- Affichage du camembert et des graphiques de corrélation ---
col1_suite, col2_suite, col3_suite = st.columns(3)

with col1_suite:
    df_pie = pd.read_parquet('data/STEP11_earthquakes.parquet')
    ressenti_counts = df_pie['ressenti'].value_counts()
    sizes = [ressenti_counts.get('non', 0), ressenti_counts.get('oui', 0)]
    labels_pie = ['Non ressenti', 'Ressenti']

    fig_pie, ax_pie = plt.subplots(figsize=(8, 6))
    ax_pie.pie(sizes, labels=labels_pie, autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#ff9999'])
    ax_pie.set_title("Proportion de séismes probablement ressentis par l'humain")
    st.pyplot(fig_pie)

    st.markdown(f'''
                
    <!-- Observation -->
    <div class="observation-box">
    <p style="margin: 0;">Un séisme est considéré probablement ressenti si sa magnitude uniformisée > 4.0, ou si sa magnitude uniformisée > 3.0 et sa profondeur < 20 km. La plupart des séismes enregistrés aux USA (2000-2005) sont non ressentis, ce qui correspond aux petits tremblements de terre constants.</p>
    </div>

    ''', unsafe_allow_html=True)

# --- Affichage des graphiques de corrélation ---
cols_corr = [
    'profondeur_km', 'mag_uniforme', 'nb_stations_localisation',
    'nb_stations_magnitude', 'ecart_azimut', 'rms',
    'erreur_horiz', 'erreur_profondeur', 'erreur_magnitude'
]
df_corr = pd.read_parquet('data/STEP11_earthquakes.parquet')
df_plot = df_corr.dropna(subset=cols_corr)

with col2_suite:
    corr_matrix = df_plot[cols_corr].corr()
    fig_corr_matrix, ax_corr = plt.subplots(figsize=(6, 5))
    im = ax_corr.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
    ax_corr.set_xticks(range(len(cols_corr)))
    ax_corr.set_yticks(range(len(cols_corr)))
    ax_corr.set_xticklabels(cols_corr, rotation=45, ha='right', fontsize=8)
    ax_corr.set_yticklabels(cols_corr, fontsize=8)
    plt.colorbar(im, ax=ax_corr, fraction=0.046, pad=0.04)
    ax_corr.set_title("Corrélation variables numériques", fontsize=10)
    plt.tight_layout()
    st.pyplot(fig_corr_matrix)
    st.markdown(f'''
    <div class="observation-box">
    <p style="margin: 0;">Corrélations notables entre certaines variables, par exemple entre le nombre de stations et la précision des mesures.</p>
    </div>
    ''', unsafe_allow_html=True)

with col3_suite:
    # Créer une figure avec 2 subplots pour les scatter plots
    fig_scatter, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8))
    
    # mag_uniforme vs nb_stations_localisation
    ax1.scatter(df_plot['mag_uniforme'], df_plot['nb_stations_localisation'], alpha=0.2, s=5)
    ax1.set_xlabel('Magnitude uniformisée')
    ax1.set_ylabel('Nb stations localisation')
    ax1.set_title('mag_uniforme / nb_stations', fontsize=10)
    
    # nb_stations_localisation vs ecart_azimut
    corr_value = df_plot['nb_stations_localisation'].corr(df_plot['ecart_azimut'])
    ax2.scatter(df_plot['nb_stations_localisation'], df_plot['ecart_azimut'], alpha=0.2, s=5)
    ax2.set_xlabel('Nb stations localisation')
    ax2.set_ylabel('Écart azimut')
    ax2.set_title(f'Corrélation (Pearson) = {corr_value:.2f}', fontsize=10)
    
    plt.tight_layout()
    st.pyplot(fig_scatter)
    
    st.markdown(f'''
    <div class="observation-box">
    <p style="margin: 0;">Les séismes de plus forte magnitude sont généralement détectés par un plus grand nombre de stations.</p>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div class="observation-box">
    <p style="margin: 0;">Plus le nombre de stations est élevé, plus l'écart azimutal tend à diminuer (meilleure couverture spatiale).</p>
    </div>
    ''', unsafe_allow_html=True)





st.divider()

st.subheader("Analyse des séismes par état entre 2000 et 2005")

# Charger les données
df_earthquakes = pd.read_parquet('data/STEP11_earthquakes.parquet')

# Charger les données géographiques des états USA
try:
    # Télécharger les shapefile des états USA depuis Natural Earth
    url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_1_states_provinces.zip"
    gdf_states = gpd.read_file(url)
    
    # Filtrer pour les états USA
    gdf_usa = gdf_states[gdf_states['admin'] == 'United States of America']
    
    # Créer un GeoDataFrame à partir des séismes
    from shapely.geometry import Point
    geometry = [Point(xy) for xy in zip(df_earthquakes['longitude'], df_earthquakes['latitude'])]
    gdf_earthquakes = gpd.GeoDataFrame(df_earthquakes, geometry=geometry, crs='EPSG:4326')
    
    # Obtenir la liste unique des états
    states_list = sorted(gdf_usa['name'].unique())
    
    # Selectbox pour choisir l'état
    selected_state = st.selectbox(
        "Sélectionnez un état :",
        options=states_list,
        index=0  # Par défaut, sélectionner le premier état
    )
    
    # Obtenir le polygon de l'état sélectionné
    state_geometry = gdf_usa[gdf_usa['name'] == selected_state].geometry.values[0]
    
    # Filtrer les séismes qui se trouvent dans l'état
    df_region_filtered = gdf_earthquakes[gdf_earthquakes.geometry.within(state_geometry)].copy()
    df_region_filtered = df_region_filtered.dropna(subset=['mag_uniforme'])
    
    if len(df_region_filtered) > 0:
        # Diviser en 2 colonnes
        col_graph, col_stats = st.columns(2)
        
        with col_graph:
            # Créer un histogramme des magnitudes uniformisées pour la région
            fig_region, ax_region = plt.subplots(figsize=(8, 5))
            ax_region.hist(df_region_filtered['mag_uniforme'], bins=30, color='#66b3ff', edgecolor='black', alpha=0.7)
            ax_region.set_xlabel('Magnitude uniformisée')
            ax_region.set_ylabel('Nombre de séismes')
            ax_region.set_title(f'Distribution des magnitudes uniformisées - {selected_state}')
            ax_region.grid(axis='y', alpha=0.3)
            st.pyplot(fig_region)
        
        with col_stats:
            # Afficher des statistiques pour la région
            stats_region = df_region_filtered['mag_uniforme'].describe()
            
            # Créer une grille HTML avec les statistiques
            stats_html = f'''
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-top: 10px;">
                <div style="background-color: {BG_COLOR}; border: 1px solid {BORDER_COLOR}; padding: 15px; border-radius: 8px; text-align: center;">
                    <p style="margin: 0; font-size: 12px; color: #999;">Nombre de séismes</p>
                    <p style="margin: 5px 0 0 0; font-size: 20px; font-weight: bold; color: {TEXT_COLOR};">{len(df_region_filtered):,}</p>
                </div>
                <div style="background-color: {BG_COLOR}; border: 1px solid {BORDER_COLOR}; padding: 15px; border-radius: 8px; text-align: center;">
                    <p style="margin: 0; font-size: 12px; color: #999;">Magnitude moyenne</p>
                    <p style="margin: 5px 0 0 0; font-size: 20px; font-weight: bold; color: {TEXT_COLOR};">{stats_region['mean']:.2f}</p>
                </div>
                <div style="background-color: {BG_COLOR}; border: 1px solid {BORDER_COLOR}; padding: 15px; border-radius: 8px; text-align: center;">
                    <p style="margin: 0; font-size: 12px; color: #999;">Magnitude médiane</p>
                    <p style="margin: 5px 0 0 0; font-size: 20px; font-weight: bold; color: {TEXT_COLOR};">{stats_region['50%']:.2f}</p>
                </div>
                <div style="background-color: {BG_COLOR}; border: 1px solid {BORDER_COLOR}; padding: 15px; border-radius: 8px; text-align: center;">
                    <p style="margin: 0; font-size: 12px; color: #999;">Magnitude min</p>
                    <p style="margin: 5px 0 0 0; font-size: 20px; font-weight: bold; color: {TEXT_COLOR};">{stats_region['min']:.2f}</p>
                </div>
                <div style="background-color: {BG_COLOR}; border: 1px solid {BORDER_COLOR}; padding: 15px; border-radius: 8px; text-align: center;">
                    <p style="margin: 0; font-size: 12px; color: #999;">Magnitude max</p>
                    <p style="margin: 5px 0 0 0; font-size: 20px; font-weight: bold; color: {TEXT_COLOR};">{stats_region['max']:.2f}</p>
                </div>
                <div style="background-color: {BG_COLOR}; border: 1px solid {BORDER_COLOR}; padding: 15px; border-radius: 8px; text-align: center;">
                    <p style="margin: 0; font-size: 12px; color: #999;">Écart-type</p>
                    <p style="margin: 5px 0 0 0; font-size: 20px; font-weight: bold; color: {TEXT_COLOR};">{stats_region['std']:.2f}</p>
                </div>
            </div>
            '''
            st.markdown(stats_html, unsafe_allow_html=True)
    else:
        st.warning(f"Aucun séisme enregistré dans {selected_state} avec magnitude uniformisée disponible.")
        
except Exception as e:
    st.error(f"Erreur lors du chargement des données géographiques: {e}")
    st.info("Assurez-vous d'avoir une connexion Internet pour télécharger les données des états USA.")

st.divider()

st.subheader("Résultat du text mining de l'article :")
st.write("https://journals.sagepub.com/doi/full/10.1177/87552930231223995")
st.write("Notebook text_mining disponible dans le dossier 'scripts'.")
st.image('assets/wordcloud.png')
    
