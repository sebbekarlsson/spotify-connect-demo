from spotifyapp.app import app

from spotifyapp.db import create_tables


create_tables()
app.run(debug=True)
