import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Charger les données depuis le fichier parquet
df = pd.read_parquet('data/STEP04_earthquakes.parquet')

# Prendre seulement les 100000 premières lignes
df = df.head(100000)

# Calculer le centre de la carte (moyenne des latitudes et longitudes)
center_lat = df['latitude'].mean()
center_lon = df['longitude'].mean()

# Créer la carte centrée sur le monde entier
m = folium.Map(location=[0, 0], zoom_start=2)

# Créer un cluster de marqueurs pour éviter la surcharge
marker_cluster = MarkerCluster().add_to(m)

# Ajouter des marqueurs pour chaque tremblement de terre
for idx, row in df.iterrows():
    # Calculer le rayon : ajouter 1 pour éviter les rayons nuls, si mag NaN, rayon=2
    if pd.isna(row['mag']):
        radius = 2
        mag_display = "non renseigné"
    else:
        radius = (row['mag'] + 1) * 2
        mag_display = f"{row['mag']}"
    
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=radius,  # Taille basée sur la magnitude
        popup=folium.Popup(f"Magnitude: {mag_display}<br>Date: {row['time'].date()}", max_width=300),
        color='red',
        fill=True,
        fill_color='red'
    ).add_to(marker_cluster)

# Sauvegarder la carte dans un fichier HTML
m.save('earthquake_map.html')

print("Carte créée et sauvegardée dans 'earthquake_map.html'")
