import io
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_auth

from app import app
from layout_data import layout0
from layout_pos import layout1
#from layout_tm import layout2
import callbacks_pos, callbacks_tm, callbacks_data

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Store(id='memory', storage_type='memory')
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'),
              State('memory', 'data'))
def display_page(pathname, data):
    if pathname == '/':
        return layout0
    elif pathname == '/app/postags':
        return layout1
#     elif pathname == '/app/topicmodel':
#          return layout2
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)