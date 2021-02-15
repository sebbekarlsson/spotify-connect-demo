from flask import Flask, redirect, request, jsonify
from spotifyapp.spotify import auth, get_new_releases


app = Flask(__name__)

app.config.update(
    SECRET_KEY='abc123',
    TEMPLATES_AUTO_RELOAD=True
)


@app.route('/callback')
def show():
    code = request.args.get('code')
    return jsonify(get_new_releases("SE", 0, 20, code))


@app.route('/auth')
def show_auth():
    return redirect(auth())
