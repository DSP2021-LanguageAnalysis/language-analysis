import os
from collections import defaultdict
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
import globals
from app import app

data_parser = globals.data_parser


layout0 = html.Div([
    html.Nav(
        className ='navbar navbar-expand-lg navbar-dark bg-primary', 
        children=[
            html.H1(className='navbar-brand', children='Data Science Project: Language variation')]
    ),
    html.H2('Create custom groups'),
    dcc.Link('POS tag visualisation', href='/app/postags'),
    dcc.Link('Topic model', href='/app/topicmodel'),
    html.Div(
        children=[
            dcc.Input(id="pos_group_name", type="text", placeholder="Name for new group"),
            dcc.Input(id="pos_group_tags", type="text", placeholder="Tags for new group as ; separated list"),
            html.Br(), 
            html.Button('Add group', id='add_pos_group_button', n_clicks = 0),
            html.Br(),
            html.Br(), 
            html.H5('The custom POS groups you have saved for this session:'),
            html.Br(), 
            html.Div(id='cust_pos_groups')
    ])
])

# line graph
@app.callback(
    Output('session', 'data'),
    Input('add_pos_group_button', 'n_clicks'),
    [State('pos_group_name', 'value')],
    [State('pos_group_tags', 'value')],
    State('session', 'data'))
def add_pos_group(n_clicks, name, tags, data):
    
    if n_clicks > 0:
        if data is None:
            data = dict()
        tags = tags.split(';')
        data[name] = dict(zip(tags, tags))
    
    return data

# line graph
@app.callback(
    Output('cust_pos_groups', 'children'),
    Input('session', 'data'))
def view_pos_groups(data):
    if data is not None:
        children = []
        for (n, t) in data.items():
            children.append(html.P('Name: {}'.format(n)))
            children.append(html.P('Tags: {}'.format(t)))
            children.append(html.Hr())
        
        return children