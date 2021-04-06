import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

import globals
globals.initialize()

from app import app
from layout_pos import layout1
from layout_tm import layout2
import callbacks_pos, callbacks_tm

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    # Parse letters to a Pandas DataFrame
    if pathname == '/app/postags':
         return layout1
    elif pathname == '/app/topicmodel':
         return layout2
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