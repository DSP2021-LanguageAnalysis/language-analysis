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
import callbacks_pos, callbacks_tm

app.layout = html.Div([
    dcc.Store(id='session', storage_type='session'),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'),
              State('session', 'data'))
def display_page(pathname, data):
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
        return '404'


if __name__ == '__main__':
    from waitress import serve
    import os
    try:
        PORT = os.environ["PORT"]
    except:
        PORT = 8050
    serve(app.server, host="0.0.0.0", port=PORT, clear_untrusted_proxy_headers=True)
