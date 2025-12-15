# Analyse des Tremblements de Terre aux USA (2000-2005)

## 📊 Description

Analyse des tremblements de terre aux USA de 2000 à 2005.
le dataset original traite des tremblements de terre dans le monde entier entre 1970 et mars 2019. Nous le travaillons pour nous concentrer sur les tremblements de terre enregistrés aux USA de 2000 à 2005 et avoir un nombre d'observations plus raisonnable. Les données proviennent de l'USGS (United States Geological Survey).

<a href="https://www.kaggle.com/datasets/danielpe/earthquakes" target="_blank">
<img src="https://www.kaggle.com/static/images/site-logo.svg" alt="Kaggle" style="height: 20px; vertical-align: middle; margin-right: 8px;"/>
<span style="display: inline-block; background: #1e2629; color: white; padding: 6px 14px; border-radius: 4px; font-size: 14px; font-weight: bold; text-decoration: none;">Voir le dataset sur Kaggle</span>
</a>

## 📁 Structure du Projet

```
projet/
├── app.py                              # Application principale Streamlit
├── README.md                           # Ce fichier
├── requirements.txt                    # Dépendances Python
│
├── assets/
│   ├── colonnes_significations.md      # Documentation des variables
│   ├── valeurs_manquantes.md           # Analyse des valeurs manquantes
│   ├── earthquake_map_areas.html       # Carte de densité (zones)
│
├── data/
│   ├── earthquakes.csv                 # Dataset brut original
│   ├── earthquakes_lite.csv            # Version allégée du dataset brut
│   ├── earthquakes_lite.parquet        # Version allégée du dataset final
│
│
├── scripts/
│   ├── create_map_areas.py             # Script pour générer la heatmap de densité
│   ├── explore_data.ipynb              # Notebook d'exploration
│   ├── prepare_data.ipynb              # Notebook de préparation des données
│   ├── text_mining.ipynb               # Notebook text mining
│   └── wordcloud.png                   # Résultat du text mining
```

## 📦 Dépendances Principales

- **streamlit** : Framework web pour l'application interactive
- **pandas** : Manipulation et analyse des données
- **geopandas** : Analyse géospatiale avec shapefiles
- **matplotlib** : Visualisations graphiques
- **folium** : Cartes interactives
- **shapely** : Opérations géométriques

---

**Dernière mise à jour** : Décembre 2025
