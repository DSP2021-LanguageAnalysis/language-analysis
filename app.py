#-*- coding: utf-8 -*-
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_bootstrap_components as dbc
from data_parser import DataParser
from topic_model import TopicModel
import time

external_stylesheets = [
        #'https://codepen.io/chriddyp/pen/bWLwgP.css'
        dbc.themes.FLATLY
    ]

# Create the app, figures and define layout
global app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

global data_parser 
data_parser = DataParser()

global topic_model
topic_model = TopicModel()