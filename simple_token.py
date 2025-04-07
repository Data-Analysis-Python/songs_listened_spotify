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
        "Content-Type" : "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "client_credentials"
    }
   
    response = post(url, headers=headers, data=data)
    result = json.loads(response.content)
    token = result['access_token']
    return token

def header():
    return {
        "Authorization": "Bearer " + get_token_spotify(),
        "Accept" : "application/json",
       "Content-Type" : "application/json",
    }

def get_information_request(url, params):
    response = get(url, params=params, headers=header())
    result = json.loads(response.content)
    return result

def categories():
    url = 'https://api.spotify.com/v1/browse/categories'
    params = {'locale': 'sv_SE', 'limit': '10', 'offset': '5'} 
    return get_information_request(url, params)

def artist():
    url = 'https://api.spotify.com/v1/search'
    params = {'q': 'Wos', 'type': 'artist', 'market': 'AR', 'limit': '5'}
    return get_information_request(url, params)

def main():
    print(categories())
    
if __name__ == "__main__":
    main()