import csv

genre_mapping = {
    'alt-rock': 'Rock', 'alternative': 'Rock', 'british': 'Rock', 'emo': 'Rock', 'grunge': 'Rock', 
    'hard-rock': 'Rock', 'j-rock': 'Rock', 'psych-rock': 'Rock', 'punk': 'Rock', 'punk-rock': 'Rock', 
    'rock': 'Rock', 'rock-n-roll': 'Rock', 'rockabilly': 'Rock', 'indie': 'Rock',
    'cantopop': 'Pop', 'indie-pop': 'Pop', 'j-idol': 'Pop', 'j-pop': 'Pop', 'k-pop': 'Pop', 
    'mandopop': 'Pop', 'pop': 'Pop', 'pop-film': 'Pop', 'power-pop': 'Pop', 'synth-pop': 'Pop',
    'breakbeat': 'Electronic', 'chicago-house': 'Electronic', 'club': 'Electronic', 'dance': 'Electronic', 
    'dancehall': 'Electronic', 'deep-house': 'Electronic', 'detroit-techno': 'Electronic', 'disco': 'Electronic', 
    'drum-and-bass': 'Electronic', 'dubstep': 'Electronic', 'edm': 'Electronic', 'electro': 'Electronic', 
    'electronic': 'Electronic', 'hardstyle': 'Electronic', 'house': 'Electronic', 'idm': 'Electronic', 
    'j-dance': 'Electronic', 'minimal-techno': 'Electronic', 'progressive-house': 'Electronic', 
    'techno': 'Electronic', 'trance': 'Electronic', 'trip-hop': 'Electronic', 'hardcore': 'Electronic',
    'black-metal': 'Metal', 'death-metal': 'Metal', 'grindcore': 'Metal', 'heavy-metal': 'Metal', 
    'industrial': 'Metal', 'metal': 'Metal', 'metalcore': 'Metal',
    'jazz': 'Jazz',
    'classical': 'Classical', 'opera': 'Classical', 'piano': 'Classical', 'show-tunes': 'Classical',
    'hip-hop': 'Hip-Hop',
    'dub': 'Reggae', 'reggae': 'Reggae', 'reggaeton': 'Reggae', 'ska': 'Reggae',
    'brazil': 'Latin', 'forro': 'Latin', 'latin': 'Latin', 'latino': 'Latin', 'mpb': 'Latin', 
    'pagode': 'Latin', 'salsa': 'Latin', 'samba': 'Latin', 'sertanejo': 'Latin', 'tango': 'Latin',
    'funk': 'Soul/R&B', 'groove': 'Soul/R&B', 'r-n-b': 'Soul/R&B', 'soul': 'Soul/R&B',
    'bluegrass': 'Folk/Country', 'country': 'Folk/Country', 'folk': 'Folk/Country', 
    'honky-tonk': 'Folk/Country', 'singer-songwriter': 'Folk/Country', 'songwriter': 'Folk/Country',
    'blues': 'Blues',
    'afrobeat': 'World', 'french': 'World', 'german': 'World', 'indian': 'World', 'iranian': 'World', 
    'malay': 'World', 'spanish': 'World', 'swedish': 'World', 'turkish': 'World', 'world-music': 'World',
    'anime': 'Kids', 'children': 'Kids', 'disney': 'Kids', 'kids': 'Kids',
    'acoustic': 'Other', 'ambient': 'Other', 'chill': 'Other', 'comedy': 'Other', 'garage': 'Other', 
    'gospel': 'Other', 'goth': 'Other', 'guitar': 'Other', 'happy': 'Other', 'new-age': 'Other', 
    'party': 'Other', 'romance': 'Other', 'sad': 'Other', 'sleep': 'Other', 'study': 'Other'
}

input_file = 'dataset.csv'
output_file = 'dataset_with_meta_genres.csv'

with open(input_file, mode='r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ['meta_genre']
    
    with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            original_genre = row['track_genre']
            row['meta_genre'] = genre_mapping.get(original_genre, 'Other')
            writer.writerow(row)

print(f"File '{output_file}' created successfully.")
