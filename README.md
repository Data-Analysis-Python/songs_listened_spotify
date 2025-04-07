# Canciones escuchadas en Spotify
ETL de canciones escuchadas en la plataforma de streaming Spotify usando Python

Pasos:
1. Se crea un endpoint para la autenticación [OAuth 2.0 de Spotify](https://developer.spotify.com/documentation/web-api/reference/get-recently-played)  utilizando Flask, la ejecución se realiza desde el script *app.py*
2. Se integra el resultado de la ejecución del paso 1, *acces_token* en el archivo *params.py*
3. Se ejecuta el script *request_with_token.py*, con el cuál vamos a obtener la información de las canciones escuchadas en spotify, en este script la se obtine la información en formato JSON, se transforma la información para guardar los datos necesarios y finalmente se insertan en una base de datos postgres.

