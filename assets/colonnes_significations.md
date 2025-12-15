# 🌍 Colonnes et significations

## 1. **time**

Moment exact du séisme.

Souvent au format ISO 8601 (ex : 2025-02-03T14:32:12.345Z).

UTC.

## 2. **latitude** / **longitude**

Coordonnées géographiques de l’épicentre du séisme.

**latitude** : Nord/Sud

**longitude** : Est/Ouest

## 3. **depth**

Profondeur de l’hypocentre du séisme sous la surface terrestre.

En kilomètres.

## 4. **mag**

Magnitude du séisme (taille/énergie).

Forme non précisée ici : peut être ML, Mw, Mb...

## 5. **magType**

Type de magnitude utilisée :

- Mw : magnitude de moment (la plus fiable)
- ML : magnitude locale (Richter)
- Mb : ondes de volume
- Md : durée

etc.

## 6. **nst**

Nombre de stations sismiques ayant détecté le séisme.

## 7. **gap**

Angle "gap" en degrés :
→ indique la couverture par les stations autour de l’épicentre.
→ plus c’est bas, meilleure est la localisation du séisme.

## 8. **dmin**

Distance horizontale minimale entre l’épicentre et la station la plus proche.

En degrés (coordonnées), pas en km.

## 9. **rms**

Résidu moyen (Root Mean Square) du modèle de localisation.

Plus c’est faible, plus la localisation est précise.

## 10. **net**

Code du réseau sismique qui a reporté l’événement.
(ex : us, ak, nc, etc.)

## 11. **id**

Identifiant unique du séisme dans la base de données.

## 12. **updated**

Date de la dernière mise à jour de l’événement (par ex. corrections apportées après analyses).

## 13. **place**

Description textuelle de la localisation.
Ex : "10 km NE of Los Angeles, California"

## 14. **type**

Type d’événement :

- earthquake
- quarry blast
- explosion
- ice quake

etc.

## 15. **horizontalError**

Incertitude horizontale (latitude/longitude) en km.

## 16. **depthError**

Incertitude sur la profondeur (en km).

## 17. **magError**

Incertitude sur la magnitude.

## 18. **magNst**

Nombre de stations utilisées spécifiquement pour calculer la magnitude.

## 19. **status**

Statut du séisme :

- automatic : détermination automatique, non révisée
- reviewed : contrôlé par un sismologue

## 20. **locationSource**

Réseau qui a fourni la localisation.

## 21. **magSource**

Réseau qui a fourni la magnitude.
