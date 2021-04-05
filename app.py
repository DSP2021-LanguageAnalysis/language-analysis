#-*- coding: utf-8 -*-
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_auth
import dash_bootstrap_components as dbc
from data_parser import DataParser

external_stylesheets = [
        #'https://codepen.io/chriddyp/pen/bWLwgP.css'
        dbc.themes.FLATLY
    ]

# Create the app, figures and define layout
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

global data_parser 
data_parser = DataParser()

app.config.suppress_callback_exceptions = True
