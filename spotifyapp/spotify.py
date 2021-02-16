from urllib.parse import urlencode
from spotifyapp.db import insert_album
from spotifyapp.config import config
import requests
import csv


CLIENT_ID = config.get('client_id')  # enter client id here

CLIENT_SECRET = config.get('client_secret')  # enter client secret here

SCOPES = ['user-read-private', 'user-read-email']
BASE_AUTH_URL = 'https://accounts.spotify.com/authorize'
REDIR = 'http://localhost:5000/callback'

BASE_BROWSE_URL = 'https://api.spotify.com/v1/browse/'
BASE_NEW_RELASES_URL = BASE_BROWSE_URL + 'new-releases'

BASE_TOKEN_URL = 'https://accounts.spotify.com/api/token'
ALBUM_BASE_URL = 'https://api.spotify.com/v1/albums/'


def get_spotify_auth_url():
    params = urlencode({
        'scopes': ','.join(SCOPES),
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIR
    })
    uri = BASE_AUTH_URL + '?' + params

    return uri


def get_new_releases(country, offset, limit, code):
    # hamtar vi auth token
    body = {
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIR,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    token_response = requests.post(BASE_TOKEN_URL, data=body)
    token_data = token_response.json()
    token = token_data.get('access_token')

    # hamtar vi new releases, och skickar med token
    params = urlencode({
        'country': country,
        'offset': offset,
        'limit': limit
    })
    uri = BASE_NEW_RELASES_URL + '?' + params
    print(uri)

    # har skickar vi med token
    headers = {'Authorization': 'Bearer ' + token}

    response = requests.get(uri, headers=headers)

    data = response.json()
    albums = data['albums']['items']

    found_albums = []

    with open('albums.csv', 'w', newline='') as csvfile:
        # loopar igenom alla album fran new-releases APIet
        for album in albums:
            album_id = album.get('id')

            if album_id:
                # plocka ut mer info om albumet genom att anropa
                # album APIet och skicka med albumet i loopens ID.
                response = requests.get(
                    ALBUM_BASE_URL + album_id, headers=headers)
                album_data = response.json()

                # sakerhetsatgerd ifall album_data ar tom
                # da hoppar vi vidare i loopen och ignorerar resten
                if not album_data:
                    continue

                album = album_data
                album['actual_artists'] = []
                found_albums.append(album)

                artists = album.get('artists', [])

                # loopa igen om alla artist i albumet
                for artist in artists:
                    artist_id = artist.get('id')

                    # sakerhetsatgerd, finns inte artist_id
                    # sa struntar vi i den artisten.
                    if not artist_id:
                        continue

                    # hamta mer info om artisten
                    response = requests.get(
                        'https://api.spotify.com/v1/artists/' + artist_id,
                        headers=headers)

                    data = response.json()

                    # stoppa in info om artisten i album objektet
                    album['actual_artists'].append(data)

            name = album['name']
            release_date = album['release_date']

            writer = csv.writer(
                csvfile,
                delimiter=';',
            )

            writer.writerow([name, release_date])

            insert_album(name, release_date)

    return found_albums
