import pandas as pd

# Lade die CSV-Datei
df = pd.read_csv('/mnt/data/data.csv')

# Transformation: Alter um 1 Jahr erhöhen
df['Alter'] = df['Alter'] + 1

# Speichere die transformierte CSV-Datei
df.to_csv('/mnt/data/transformed_data.csv', index=False)

print("CSV transformiert und gespeichert!")
