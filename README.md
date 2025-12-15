# Analyse des Tremblements de Terre aux USA (2000-2005)

## 📊 Description

Cette application Streamlit offre une analyse complète des tremblements de terre enregistrés aux États-Unis entre 2000 et 2005. Elle combine des données du USGS (United States Geological Survey) avec des visualisations interactives pour explorer les patterns sismiques régionaux.

## 🎯 Fonctionnalités Principales

### 1. **Informations sur le Dataset**

- **Données brutes** : 380,123 observations du dataset initial
- **Données nettoyées** : Parquet optimisé avec toutes les transformations appliquées
- Section détaillée sur les étapes de nettoyage et normalisation

### 2. **Carte de Densité Sismique**

- Visualisation interactive des tremblements de terre sur une carte
- Coloration des régions basée sur le nombre de séismes
- Dégradation de couleur : jaune (peu de séismes) → rouge (beaucoup de séismes)

### 3. **Statistiques Descriptives Globales**

- **Boxplot** : Distribution des magnitudes uniformisées
- **Graphique en barres** : Types de magnitude utilisés
- **Histogramme** : Répartition par catégories de magnitude
- **Camembert** : Proportion de séismes probablement ressentis
- **Matrices de corrélation** : Relations entre variables numériques
- **Scatter plots** : Visualisations bivariées

### 4. **Analyse Régionale Interactive**

- Dropdown pour sélectionner un état américain
- Histogramme en temps réel des magnitudes pour l'état sélectionné
- Grille statistique avec 6 métriques clés :
  - Nombre de séismes
  - Magnitude moyenne
  - Magnitude médiane
  - Magnitude min/max
  - Écart-type

### 5. **Text Mining**

- Analyse textuelle des descriptions de localisation
- Wordcloud généré à partir des données

## 📁 Structure du Projet

```
projet2/
├── app.py                              # Application principale Streamlit
├── README.md                           # Ce fichier
├── requirements.txt                    # Dépendances Python
├── colonnes_significations.md          # Documentation des variables
├── valeurs_manquantes.md               # Analyse des valeurs manquantes
├── prepare_data.ipynb                  # Notebook de préparation des données
├── explore_data.ipynb                  # Notebook d'exploration
├── text_mining.ipynb                   # Notebook text mining
│
├── data/
│   ├── earthquakes.csv                 # Dataset brut original
│   ├── earthquakes_lite.csv            # Version allégée du dataset brut
│   ├── earthquakes_lite.parquet        # Version parquet allégée
│   └── STEP11_earthquakes.parquet      # Dataset final nettoyé
│
├── others/
│   ├── create_usa_map.py               # Script pour générer la carte des états
│   ├── usa_earthquake_map.html         # Carte interactive avec densité sismique
│   └── test.py                         # Fichiers de test
│
└── scripts/
    └── wordcloud.png                   # Résultat du text mining
```

## 🚀 Installation et Utilisation

### Prérequis

- Python 3.8+
- pip ou conda

### Installation

1. **Cloner le projet**

```bash
cd projet2
```

2. **Créer un environnement virtuel**

```bash
python -m venv venv
source venv/Scripts/activate  # Sur Windows
# ou
source venv/bin/activate  # Sur macOS/Linux
```

3. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

### Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à `http://localhost:8501`

## 📦 Dépendances Principales

- **streamlit** : Framework web pour l'application interactive
- **pandas** : Manipulation et analyse des données
- **geopandas** : Analyse géospatiale avec shapefiles
- **matplotlib** : Visualisations graphiques
- **folium** : Cartes interactives
- **shapely** : Opérations géométriques

## 📊 Structure des Données

### Colonnes du Dataset Final

| Colonne                    | Type       | Description                                |
| -------------------------- | ---------- | ------------------------------------------ |
| `date`                     | datetime64 | Date/heure du séisme (UTC)                 |
| `latitude`                 | Float64    | Latitude de l'épicentre                    |
| `longitude`                | Float64    | Longitude de l'épicentre                   |
| `profondeur_km`            | Float64    | Profondeur en kilomètres                   |
| `magnitude`                | Float64    | Magnitude brute du séisme                  |
| `type_magnitude`           | string     | Type de magnitude (Mw, ML, Mb, etc.)       |
| `mag_uniforme`             | Float64    | **Magnitude normalisée** pour comparaisons |
| `nb_stations_localisation` | Int64      | Nombre de stations pour la localisation    |
| `nb_stations_magnitude`    | Int64      | Nombre de stations pour la magnitude       |
| `ecart_azimut`             | Float64    | Couverture azimutale des stations          |
| `rms`                      | Float64    | Résidu du modèle de localisation           |
| `erreur_horiz`             | Float64    | Incertitude horizontale (km)               |
| `erreur_profondeur`        | Float64    | Incertitude sur la profondeur (km)         |
| `erreur_magnitude`         | Float64    | Incertitude sur la magnitude               |
| `lieu`                     | string     | Description textuelle du lieu              |
| `ressenti`                 | string     | Probabilité d'être ressenti (oui/non)      |
| `ID`                       | string     | Identifiant unique du séisme               |
| `date_maj_infos`           | datetime64 | Date de dernière mise à jour               |

## 🧹 Étapes de Nettoyage Appliquées

1. **Conversion des types** : Dates, nombres, catégories
2. **Suppression des doublons** : Strictement identiques et sur l'ID unique
3. **Standardisation NaN** : Conversion des 0 "informations manquantes" en NaN
4. **Normalisation des lieux** : Regroupement avec suppression des accents et ponctuation
5. **Magnitude uniforme** : Normalisation selon le type pour comparabilité
6. **Suppression de colonnes** : Colonnes non utilisées (net, locationSource, etc.)
7. **Renommage français** : Pour une meilleure lisibilité
8. **Filtrage** : USA + rayon de 50 km, années 2000-2005, séismes uniquement
9. **Colonne ressenti** : Basée sur magnitude et profondeur

## 📈 Points Clés de l'Analyse

### Observations Principales

- **Magnitude** : La majorité des séismes (> 90%) ont une magnitude uniformisée < 2
- **Localisation** : Alaska et Californie sont les états avec le plus de séismes
- **Détection** : Les séismes de forte magnitude sont détectés par plus de stations
- **Qualité** : Plus de stations = meilleure couverture azimutale
- **Ressenti** : La plupart des séismes enregistrés ne sont pas ressentis par les humains

### Corrélations Notables

- Magnitude ↔ Nombre de stations (r > 0.3)
- Nombre de stations ↔ Écart azimut (r > 0.7)
- Profondeur ↔ Magnitude (r > 0.2)

## 🗺️ Carte Interactive des États

La carte HTML (`usa_earthquake_map.html`) affiche :

- **Toutes les limites des états USA**
- **Coloration basée sur la densité sismique**
- **Popups** affichant le nombre de séismes par état au clic
- **Légende** avec dégradation de couleur (jaune → rouge)

## 📝 Notes sur les Données Manquantes

Certaines colonnes contiennent des valeurs manquantes pour des raisons légitimes :

- `mag_uniforme` : Certains types de magnitude ne peuvent pas être normalisés
- `nb_stations_magnitude` et `nb_stations_localisation` : Données non disponibles pour certains séismes
- `erreur_*` : Calculs impossibles pour certains événements

Voir `valeurs_manquantes.md` pour plus de détails.

## 📚 Ressources

- **Dataset original** : [Kaggle - Earthquakes Dataset](https://www.kaggle.com/datasets/danielpe/earthquakes)
- **Source des données** : [USGS Earthquake Hazards Program](https://earthquake.usgs.gov/)
- **Shapefiles** : [Natural Earth Data](https://www.naturalearthdata.com/)

## 👨‍💻 Auteur

Projet de visualisation de données - Sorbonne Université

## 📄 Licence

Données publiques (USGS)

---

**Dernière mise à jour** : Décembre 2025
