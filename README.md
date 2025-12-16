# Analyse des Tremblements de Terre aux USA (2000-2005)

## 📊 Description

Analyse des tremblements de terre aux USA de 2000 à 2005.
Le dataset original traite des tremblements de terre dans le monde entier entre 1970 et mars 2019. Nous le travaillons pour nous concentrer sur les tremblements de terre enregistrés aux USA de 2000 à 2005 et avoir un nombre d'observations plus raisonnable. Les données proviennent de l'USGS (United States Geological Survey).

<a href="https://www.kaggle.com/datasets/danielpe/earthquakes" target="_blank">
<img src="https://www.kaggle.com/static/images/site-logo.svg" alt="Kaggle" style="height: 20px; vertical-align: middle; margin-right: 8px;"/>
<span style="display: inline-block; background: #1e2629; color: white; padding: 6px 14px; border-radius: 4px; font-size: 14px; font-weight: bold; text-decoration: none;">Voir le dataset sur Kaggle</span>
</a>

## ⚠️ Important

> **Avant de lancer l'application Streamlit**, vous devez exécuter toutes les cellules (run all) du notebook 'scripts\prepare_data.ipynb' pour préparer les données. Les données brutes sont téléchargées et nettoyées.

## 📁 Structure du Projet

```
projet/
├── app.py                              # Application principale Streamlit
├── requirements.txt                    # Dépendances Python
│
├── assets/
│   ├── colonnes_significations.md      # Documentation des variables
│   ├── valeurs_manquantes.md           # Analyse des valeurs manquantes
│   ├── earthquake_map_areas.html       # Carte de densité (zones)
│   └── wordcloud.png                   # Résultat du text mining
│
├── data/                               # sera généré avec le notebook
│
├── scripts/
│   ├── create_map_areas.py             # Script pour générer la heatmap de densité
│   ├── explore_data.ipynb              # Notebook d'exploration
│   ├── prepare_data.ipynb              # Notebook de préparation des données
│   └── text_mining.ipynb               # Notebook text mining
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
