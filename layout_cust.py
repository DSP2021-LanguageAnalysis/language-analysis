import os
from collections import defaultdict
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
import globals
from app import app

data_parser = globals.data_parser


layout0 = html.Div([
    dbc.Nav(
        className ='navbar navbar-expand-lg navbar-dark bg-primary', 
        children=[
            html.H1(className='navbar-brand', children='VARIENG: TCEECE corpus analysis'),
            dbc.NavItem(dbc.NavLink('Overview', href='/app/overview')),
            dbc.NavItem(dbc.NavLink('POS tag analysis', href='/app/postags')),
            dbc.NavItem(dbc.NavLink('Topic model', href='/app/topicmodel')),
            dbc.NavItem(dbc.NavLink('Add custom groups', active=True, href='/app/customize'))
        ],
        pills=True
    ),
    dcc.Tabs([
        dcc.Tab(
            label='Instructions',
            children=[
                html.Div(
                    style={'padding': '20px'},
                    children=[
                        html.H2("User instructions"),
                        #dcc.Link('link to github with more detailed documentation', href='https://github.com/DSP2021-LanguageAnalysis/language-analysis'),
                        dcc.Markdown(''' 
                        - [Link to github with more detailed documentation](https://github.com/DSP2021-LanguageAnalysis/language-analysis)
                        - Select attribute that you want to create a custom grouping for with the tabs
                        - Note: There are already some premade groupings for convenience 
                        - **Pre-Made Class Grouping Classifications**
                                - **Fine grained** - Royalty (R) , Nobility (N) , Gentry Upper (GU), Gentry Lower (GL, G), Clergy Upper (CU), Clergy Lower (CL), Professional (P), Merchant (M), Other (O)
                                - **Regular** - Royalty (R) , Nobility (N) , Gentry (GU, GL, G), Clergy (CU, CL), Professional (P), Merchant (M), Other (O)
                                - **Tripartite** - Upper (R, N, GU, GL, G, CU), Middle (CL, P, M), Lower (O)
                                - **Bipartite** - Gentry (R, N, GU, GL, G, CU), Non-Gentry (CL, P, M, O)
                        - **POS tags**
                            - [Link to Constituent Likelihood Automatic Word-tagging System (CLAWS7) tagset](http://ucrel.lancs.ac.uk/claws7tags.html)
                            - The ditto tags that are present in the corpus are included when the main tag is selected. 
                            I.e. if user selects to see tag NN1 then ditto tags NN121, NN122, NN131, NN132, NN133 are also included.
                            - Note: The tags NPM2 (plural month noun) and MCGE (genitive cardinal number, neutral for number) have been removed from selection, 
                            as they are not featured in this particular corpus.
                        - **POS tag tab**
                            - Type name for new custom grouping
                            - Write POS tags to be included in your group, separated by the ";" symbol
                            - Example: N;NN;NN1
                            - Click **Add Group** to save the group for the current app session
                            - Now the custom group is included as an option in the POS tag filtration options for both the POS analysis and Topic modelling tabs
                        - **Other tab**
                            - Coming soon
                            ''')
                        ])
                ]
            ),
        dcc.Tab(
            label='POS',
            children=[
                html.Div(
                    style={'padding': '20px'},
                    children=[
                        html.H5('Add a new custom POS grouping'),
                        dcc.Input(id="pos_group_name", type="text", placeholder="Name for new group"),
                        dcc.Input(id="pos_group_tags", type="text", placeholder="Tags for new group as ; separated list", style={'width': '100%'}),
                        html.Br(), 
                        html.Button('Add group', id='add_pos_group_button', n_clicks = 0),
                        html.Br(),
                        html.Br(), 
                        html.P('The custom POS groups you have saved for this session', style={'fontWeight':'bold'}),
                        html.Div(id='cust_pos_groups')])]),
        dcc.Tab(
            label='Other',
            children=[
                html.Div(
                    style={'padding': '20px'},
                    children=[
                        html.H5('You can later add other groups as well.')])])
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
        data[name] = tags
    
    return data

# line graph
@app.callback(
    Output('cust_pos_groups', 'children'),
    Input('session', 'data'))
def view_pos_groups(data):
    if data is not None:
        children = []
        for (n, t) in data.items():
            children.append(html.P('{}: {}'.format(n, ', '.join(list(t)))))
        
        return children
