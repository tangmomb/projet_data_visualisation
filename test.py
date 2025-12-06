import pandas as pd
df = pd.read_csv('csv/earthquakes.csv')

# tout convertir
df = df.convert_dtypes()

# puis les dates
date_columns = ['time', 'updated']
for col in date_columns:
    df[col] = pd.to_datetime(df[col], utc=True, errors='coerce')

df.dtypes

df.to_parquet('csv/earthquakes.parquet')