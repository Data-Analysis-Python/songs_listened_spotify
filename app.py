import urllib
import params

from requests import post
from flask import Flask, redirect, request, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    autentication_request_params = {
        'response_type': 'code',
        'client_id': params.CLIENT_ID,
        'redirect_uri': params.REDIRECT_URI,
        'scope': 'user-read-recently-played user-top-read',
        'show_dialog': 'true'
    }

    auth_url = 'https://accounts.spotify.com/authorize/?' + urllib.parse.urlencode(autentication_request_params)
    return redirect(auth_url)

def get_access_token(authorization_code:str):
    body = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'client_id': params.CLIENT_ID,
        'client_secret': params.CLIENT_SECRET,
        'redirect_uri': params.REDIRECT_URI
    }

    spotify_request_access_token_url = 'https://accounts.spotify.com/api/token/?'

    response = post(spotify_request_access_token_url, data=body)
    if response.status_code == 200:
        return response.json()
    raise Exception ('No se puedo obtener el token de acceso')
    
@app.route('/callback')
def callback():
    code = request.args.get('code')
    credentials = get_access_token(authorization_code=code)
    return jsonify({'access_token': credentials['access_token']})

if __name__ == '__main__':
    app.run(debug=True)
