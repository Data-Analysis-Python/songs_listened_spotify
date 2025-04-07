import datetime
import requests
import params 
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

def check_if_valid_data(df: pd.DataFrame) -> bool:
    if df.empty:
        print("No existes registros por procesar")
        return False
    
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception("Primary Key duplicada")
    
    if df.isnull().values.any():
        raise Exception("Se encontraron valores nulos")

def get_recently_played():
    '''
     Description: 
     Args:
     Retrun:
    '''
    
    url = "https://api.spotify.com/v1/me/player/recently-played"
    headers = {
        "Authorization" : "Bearer {}".format(params.ACCESS_TOKEN)
    }

    yesterday = datetime.datetime.now() - datetime.timedelta(days=100)
    yesterday_unix_timestamp = int(yesterday.timestamp() * 1000)
    query = f"&after={yesterday_unix_timestamp}"
    print(url + query, headers)
    response = requests.get(url, headers=headers)
    result = response.json()
    return result

def get_data_frame():
    result = get_recently_played()
    song_names, artist_names, played_at_list, timestamps = [], [], [], []

    for song in result['items']:
        song_names.append(song['track']['name'])
        artist_names.append(song['track']['album']['artists'][0]['name'])
        played_at_list.append(song['played_at'])
        timestamps.append(song['played_at'][0:10])

    song_dict = {
        'song_name': song_names,
        'artist_name': artist_names,
        'played_at': played_at_list,
        'timestamp': timestamps
    }

    song_df = pd.DataFrame(song_dict, columns=['song_name', 'artist_name', 'played_at', 'timestamp'])
    return song_df

def save_data():
    engine = create_engine(f"postgresql+psycopg2://{params.DB_USER}:{params.DB_PASS}@{params.DB_HOST}:{params.DB_PORT}/{params.DB_NAME}")
    
    try:   
        engine.execute("""
            CREATE TABLE IF NOT EXISTS played_tracks(
                    song_name VARCHAR(200),
                    artist_name VARCHAR(200),
                    played_at VARCHAR(200),
                    timestamp VARCHAR(200),
                    CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
            );
        """)
        print('Base de datos creada.')
    
        song_df = get_data_frame()
        song_df.to_sql('played_tracks', engine, index=False, if_exists='append')
        print('Datos insertados.')

    except psycopg2.Error as e:
        print(f'Error de conexión: {e}')

def main():
    save_data()
    
    # if check_if_valid_data(get_data_frame()):
    #     print("Data frame válido.")
    #     print(get_data_frame())
    
if __name__ == "__main__":
    main()
