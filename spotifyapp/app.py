from flask import Flask, redirect, request, jsonify
from spotifyapp.spotify import get_spotify_auth_url, get_new_releases


app = Flask(__name__)

app.config.update(
    SECRET_KEY='abc123',
    TEMPLATES_AUTO_RELOAD=True
)


# spotify sends the user here after clicking "agree" on sign-in page.
@app.route('/callback')
def show():
    # we need to grab the `code` variable from the URL to
    # use spotify's API later on.
    code = request.args.get('code')

    # calling our own function to fetch latest releases through
    # spotify API
    releases = get_new_releases("SE", 0, 20, code)

    # show the relases to the user in the browser
    return jsonify(releases)


# User goes here in our application when they want to sign in
@app.route('/auth')
def show_auth():
    # Calling our own function to generate a proper URL for authentication
    auth_url = get_spotify_auth_url()

    # Redirect the user to spotify's login page.
    return redirect(auth_url)
