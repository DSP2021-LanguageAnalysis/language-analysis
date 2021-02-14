# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_auth
import plotly.express as px
import pandas as pd
from data_parser import DataParser

# Keep this out of source code repository - save in a file or a database
# Here just to demonstrate this authentication possibility
VALID_USERNAME_PASSWORD_PAIRS = {
    'user': 'user'
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def create_dataframes():
    # Parse letters to a Pandas DataFrame
    data_parser = DataParser()
    df = data_parser.letters_to_df()

    # Word count DataFrame
    word_counts = df.groupby(['ID', 'Year']).size().to_frame(name = 'word_count').reset_index()

    # POS counts for each letter
    pos_counts = df.groupby(['ID', 'Tags', 'Year']).size().to_frame(name = 'pos_count').reset_index()

    # NN1 tag count per year
    nn1_counts = pos_counts[pos_counts['Tags'] == 'NN1']
    nn1_counts = nn1_counts.groupby(['Year']).size().to_frame(name = 'nn1_count').reset_index()

    return word_counts, pos_counts, nn1_counts


# Create the app, figures and define layout
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
word_counts, pos_counts, nn1_counts = create_dataframes()

wc_fig = px.scatter(word_counts, x="Year", y="word_count")
pc_fig = px.line(nn1_counts, x="Year", y="nn1_count")

app.layout = html.Div(children=[
    html.H1(children='Data Science Project: Language variation'),

    dcc.Graph(
        id='word-count-graph',
        figure=wc_fig
    )
    , dcc.Graph(
        id='pos-count-graph',
        figure=pc_fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
