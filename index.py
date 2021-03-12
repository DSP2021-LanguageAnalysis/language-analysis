import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import dash_auth

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
    app.run_server(debug=True)