import pandas as pd
import sqlite3
import json
import sys

# Le dataset_for_machine.csv est ma nouvelle base
df = pd.read_csv('data/dataset_for_machine.csv')

# Prenant les track_id donné au lancement du script (python3 04-recommand.py id1 id2 id3 id4 etc...)
seed_tracks = sys.argv[1:]

# Extraire les lignes de la Seed Playlist
seedRows = df[df['track_id'].isin(seed_tracks)]

# On isole uniquement les colonnes numériques de la Seed Playlist
cols_numeriques = seedRows.select_dtypes(include=['number', 'bool'])

# On calcule l'écart-type de toutes ces colonnes
# Le paramètre ddof=0 force la division par N au lieu de N-1 sur la formule std() initiale
ecarts_types = cols_numeriques.std(ddof=0)
averages = cols_numeriques.mean()

# On créé une matrice de poids
weightsMatrix = {}

# Soustrait chaque élément de la série à 1.0
weightsMatrix = 1.0 - ecarts_types


# Hiérarchie des colonnes
primaryColumns = [
    'energy',
    'speechiness',
    'acousticness',
    'instrumentalness',
    'valence'
]
secondaryColumns = [
    'popularity',
    'danceability',
    'tempo',
    'liveness',
    'duration_ms',
]
tertiaryColumns = [
    'loudness',
    'explicit'
]

# Application de la hiérarchie (Multiplicateurs par colonne)
for col in weightsMatrix.index:
    
    # Normalisation des colonnes binaires
    # Calcul : (1.0 - ecart_type) * moyenne * poids + 0.1 (<- pour empêcher de finir à 0.0)
    if col.startswith('genre_'):
        # On divise par 2 l'importance de tous les genres (Poids max = 0.5)
        weightsMatrix[col] = weightsMatrix[col] * averages[col] * 1 + 0.1
        
    elif col.startswith('ts_'):
        # La métrique (time signature) est encore moins prioritaire
        weightsMatrix[col] = weightsMatrix[col] * averages[col] * 0.5 + 0.1
        
    elif col == 'mode':
        # La métrique mode (majeur, mineur) arrive trop facilement à 1
        weightsMatrix[col] = weightsMatrix[col] * averages[col] * 0.8 + 0.1
        
    else:
        # Les features audio pures (energy, valence...) gardent 100% de leur poids
        weightsMatrix[col] *= 1.0
        
    # Normalisation des colonnes les plus importantes
    if col in primaryColumns:
        weightsMatrix[col] *= 1.0
    
    # Normalisation des colonnes secondaires    
    elif col in secondaryColumns:
        weightsMatrix[col] *= 0.8
    
    # Normalisation des colonnes les moins importantes    
    elif col in tertiaryColumns:
        weightsMatrix[col] *= 0.6
        

# Affichage des poids les plus forts pour vérifier ta hiérarchie
print(weightsMatrix.sort_values(ascending=False))



# Création du Vecteur Cible
# On fusionne les 3 morceaux en utilisant la moyenne de chaque colonne numérique
idealVector = averages.copy()

# On multiplie directement la cible par les poids (Vectorisation)
weightedIdealVector = idealVector * weightsMatrix

# Pondération de l'Univers
# On isole l'id pour ne garder que les nombres du dataset complet
numberedUniverse = df.select_dtypes(include=['number', 'bool'])

weightedUniverse = numberedUniverse * weightsMatrix


# Calcul de la distance entre chaque morceau et la seed
squared_differences = (weightedUniverse - weightedIdealVector) **2
finalResult = squared_differences.sum(axis=1) **0.5

# Mettre l'id et la distance dans un nouveau tableau clair
recommendations = pd.DataFrame({
    'track_id': df['track_id'],
    'distance': finalResult
})

# Trier les valeurs
recommendations.sort_values(ascending=True, by='distance', inplace=True)

# Enlever les tracks de la Seed Playlist
final_df = recommendations[~recommendations['track_id'].isin(seed_tracks)]

# 5 meilleures recommandations
final_df.head(5)

# Mettre les ids dans une liste
track_ids = final_df.head(5)['track_id'].tolist()

print(track_ids)

sqlQuery = "SELECT track_name, artists FROM songs WHERE track_id IN (?, ?, ?, ?, ?)"

# Connexion à SQLite
conn = sqlite3.connect('data/music_database.db')
cursor = conn.cursor()

cursor.execute(sqlQuery, track_ids)

# Récupération des données dans une liste de tuples
rawResults = cursor.fetchall()

# Fermeture de la connexion
conn.close()

finalTable = pd.DataFrame(rawResults, columns=['track_name', 'artists'])

print(finalTable)

# Création de l'output JSON
finalDictionnary = {}

# iterrows() permet de boucler sur un DataFrame ligne par ligne
for index, row in finalTable.iterrows():
    keyName = f"song{index + 1}" # Va créer song1, song2...
    
    finalDictionnary[keyName] = {
        "track_name": row["track_name"],
        "artists": row["artists"]
    }

# Ouvre un fichier en mode écriture ('w' pour write)    
with open("data/recommendations.json", "w", encoding='utf-8') as file:
    # json.dump convertit le dictionnaire Python en vrai texte JSON
    # indent=4 permet de le formater proprement avec des sauts de ligne
    json.dump(finalDictionnary, file, indent=4)

print("Le fichier data/recommendations.json a été créé avec succès !")
