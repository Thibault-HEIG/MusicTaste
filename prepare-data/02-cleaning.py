import pandas as pd

# Le dataset_cleaned.csv est ma nouvelle base
df = pd.read_csv('dataset_cleaned.csv')

# Mapping min-max
def mappingMinMax(column):
    normalized_column = (df[column] - df[column].min()) / (df[column].max() - df[column].min())
    df[column] = normalized_column
    return

columnsToMap = ["tempo", "duration_ms", "loudness", "speechiness", "instrumentalness", "liveness"]

for col in columnsToMap:
    mappingMinMax(col)
    
# Transformer le booléen en int (0, 1)
df["explicit"] = df["explicit"].astype(int)

# Création des colonnes binaires pour les genres et time_signatures
df = pd.get_dummies(df, columns=['meta_genre', 'time_signature'], prefix=['genre', 'ts'])

# Sélectionner uniquement les colonnes numériques + l'ID
cols_numeriques = df.select_dtypes(include=['number']).columns.tolist()
df = df[['track_id'] + cols_numeriques]

# On créé une copie du CSV pour l'algorithme
df.to_csv('dataset_for_machine.csv', index=False)
print("Le CSV est prêt à être utilisé pour l'algorithme : dataset_for_machine.csv")

print("Les données ont été normalisées et transformées en nombres.")