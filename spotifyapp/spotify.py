from urllib.parse import urlencode
import requests
import csv


CLIENT_ID = ''  # enter client id here

CLIENT_SECRET = ''  # enter client secret here

SCOPES = ['user-read-private', 'user-read-email']
BASE_AUTH_URL = 'https://accounts.spotify.com/authorize'
REDIR = 'http://localhost:5000/callback'

BASE_BROWSE_URL = 'https://api.spotify.com/v1/browse/'
BASE_NEW_RELASES_URL = BASE_BROWSE_URL + 'new-releases'

BASE_TOKEN_URL = 'https://accounts.spotify.com/api/token'


def auth():
    params = urlencode({
        'scopes': ','.join(SCOPES),
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIR
    })
    uri = BASE_AUTH_URL + '?' + params

    print(uri)

    return uri


def get_new_releases(country, offset, limit, code):
    body = {
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIR,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    token_uri = BASE_TOKEN_URL
    token_response = requests.post(token_uri, data=body)
    token_data = token_response.json()
    token = token_data.get('access_token')
    params = urlencode({
        'country': country,
        'offset': offset,
        'limit': limit
    })
    uri = BASE_NEW_RELASES_URL + '?' + params
    headerz = {'Authorization': 'Bearer ' + token}
    response = requests.get(uri, headers=headerz)

    data = response.json()
    albums = data['albums']['items']

    with open('albums.csv', 'w', newline='') as csvfile:
        for album in albums:
            name = album['name']
            release_date = album['release_date']

            writer = csv.writer(
                csvfile,
                delimiter=' ',
                quotechar='|',
                quoting=csv.QUOTE_MINIMAL
            )

            writer.writerow([name, release_date])

    return response.json()
