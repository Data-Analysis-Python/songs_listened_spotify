import datetime
import requests
import params 
import pandas as pd

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

    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
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

def main():
    print(get_data_frame())
    
if __name__ == "__main__":
    main()
