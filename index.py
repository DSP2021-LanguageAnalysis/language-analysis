import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd

import globals
globals.initialize()

from app import app
from layout_cust import layout0
from layout_pos import layout1
from layout_tm import layout2
from layout_overview import layout3
from layout_404 import layout404
import callbacks_pos, callbacks_tm, callbacks_cust

app.layout = html.Div([
    dcc.Store(id='user-pos-store', storage_type='local'),
    dcc.Store(id='user-relationship-store', storage_type='local'),
    dcc.Store(id='user-rank-store', storage_type='local'),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    # Parse letters to a Pandas DataFrame
    if pathname == '/app/customize':
        return layout0
    elif pathname == '/app/postags':
        return layout1
    elif pathname == '/app/topicmodel':
        return layout2
    elif pathname == '/app/overview':
        return layout3
    else:
        return layout404


if __name__ == '__main__':
    app.run_server(debug=True)
