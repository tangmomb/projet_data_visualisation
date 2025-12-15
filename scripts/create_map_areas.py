
import pandas as pd
import folium
from folium.plugins import HeatMap

# Charger les données depuis le fichier parquet
df = pd.read_parquet('data/STEP11_earthquakes.parquet')

# Créer la carte centrée sur le continent nord-américain
m = folium.Map(location=[54, -105], zoom_start=3)

# Filtrer pour ne garder que les séismes avec mag_uniforme > 3
df_filtered = df[df['mag_uniforme'] > 3]
# Préparer les données pour la heatmap (zones de densité)
heat_data = df_filtered[['latitude', 'longitude']].dropna().values.tolist()

# Ajouter la heatmap à la carte
HeatMap(heat_data, radius=12, blur=15, min_opacity=0.3, max_zoom=7).add_to(m)

# Sauvegarder la carte dans un fichier HTML
m.save('assets/earthquake_map_areas.html')

print("Carte créée et sauvegardée dans 'assets/earthquake_map_areas.html'")