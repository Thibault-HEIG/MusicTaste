SELECT artists, track_name, track_id FROM songs
ORDER BY popularity DESC
LIMIT 100;

SELECT COUNT(*) FROM songs;

SELECT COUNT(*), meta_genre FROM songs GROUP BY meta_genre ORDER BY COUNT(*) DESC;

SELECT track_name FROM songs WHERE track_id = '4U45aEWtQhrm8A5mxPaFZ7';