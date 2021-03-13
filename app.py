#-*- coding: utf-8 -*-
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_auth
import dash_bootstrap_components as dbc
from flask_caching import Cache

external_stylesheets = [
        #'https://codepen.io/chriddyp/pen/bWLwgP.css'
        dbc.themes.FLATLY
    ]

# Create the app, figures and define layout
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})

app.config.suppress_callback_exceptions = True


# Keep this out of source code repository - save in a file or a database
# Here just to demonstrate this authentication possibility
VALID_USERNAME_PASSWORD_PAIRS = {
    'user': 'user'
}

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)