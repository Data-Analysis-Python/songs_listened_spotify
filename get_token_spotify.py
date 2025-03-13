import base64
import pandas as pd
from requests import post, get
import json
from datetime import datetime
import datetime
import params

def get_token_spotify():
    auth = f"{params.CLIENT_ID}:{params.CLIENT_SECRET}"
    auth_bytes = auth.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    data = {"grant_type":"client_credentials"}
   
    response = post(url, headers=headers, data=data)
    result = json.loads(response.content)
    token = result['access_token']
    return token

def auth_header():
    token = get_token_spotify()
    return {"Authorization": "Beare " + token}

def get_song_spotify():
    endpoint = "https://api.spotify.com/v1/me/player/recently-played"


def main():
    pass
    

if __name__ == "__main__":
    main()