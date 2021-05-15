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
                        #dcc.Link('link to github with more detailed documentation', href='https://github.com/DSP2021-LanguageAnalysis/language-analysis'),
                        dcc.Markdown(''' 
                        [Link to github with more detailed documentation](https://github.com/DSP2021-LanguageAnalysis/language-analysis)
                        
                        [Link to Constituent Likelihood Automatic Word-tagging System (CLAWS7) tagset](http://ucrel.lancs.ac.uk/claws7tags.html)

                        - Select attribute that you want to create a custom grouping for with the tabs
                        - Note: There are already some premade groupings for convenience 
                        - Social rank of sender, pre-made groupings available:
                            - **Fine grained** - Royalty (R) , Nobility (N) , Gentry Upper (GU), Gentry Lower (GL, G), Clergy Upper (CU), Clergy Lower (CL), Professional (P), Merchant (M), Other (O)
                            - **Regular** - Royalty (R) , Nobility (N) , Gentry (GU, GL, G), Clergy (CU, CL), Professional (P), Merchant (M), Other (O)
                            - **Tripartite** - Upper (R, N, GU, GL, G, CU), Middle (CL, P, M), Lower (O)
                            - **Bipartite** - Gentry (R, N, GU, GL, G, CU), Non-Gentry (CL, P, M, O)
                        - Relationship between sender and recipient, pre-made groupings available:
                            - **Fine grained** - Nuclear family (FN) , Other family (FO) , Family servant (FS), Close friend (TC), Other acquaintance (T)
                            - **Bipartite** - Family (FN, FO, FS) , Other (TC, T)       
                        
                        #### POS tag, relationship, and rank tabs
                        - Select the tab of the attribute you would like to create a custom group for
                        - Type name for new custom grouping
                        - Write POS, relationship, or rank tags to be included in your group, separated by the ";" symbol
                        - Example - in the POS tag tab: N;NN;NN1
                        - Click **Add group** to save the group for the current app session
                        - Now the custom group is included as an option in the POS tag filtration options for both the POS tag analysis and Topic modelling tabs
                        - **Note:** For the POS tags, the ditto tags that are present in the corpus are included when the main tag is selected. 
                        I.e. if user selects to see tag NN1 then ditto tags NN121, NN122, NN131, NN132, NN133 are also included.
                        - **Note:** The tags NPM2 (plural month noun) and MCGE (genitive cardinal number, neutral for number) have been removed from selection, 
                        as they are not featured in this particular corpus
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
            label='Relationships',
            children=[
                html.Div(
                    style={'padding': '20px'},
                    children=[
                        html.H5('Add a new custom relationship grouping'),
                        dcc.Input(id="relationship_group_name", type="text", placeholder="Name for new group"),
                        dcc.Input(id="relationship_group_tags", type="text", placeholder="Tags for new group as ; separated list", style={'width': '100%'}),
                        html.Br(), 
                        html.Button('Add group', id='add_relationship_group_button', n_clicks = 0),
                        html.Br(),
                        html.Br(), 
                        html.P('The custom relationship groups you have saved for this session', style={'fontWeight':'bold'}),
                        html.Div(id='cust_relationship_groups')])]),
        dcc.Tab(
            label='Ranks',
            children=[
                html.Div(
                    style={'padding': '20px'},
                    children=[
                        html.H5('Add a new custom rank grouping'),
                        dcc.Input(id="rank_group_name", type="text", placeholder="Name for new group"),
                        dcc.Input(id="rank_group_tags", type="text", placeholder="Tags for new group as ; separated list", style={'width': '100%'}),
                        html.Br(), 
                        html.Button('Add group', id='add_rank_group_button', n_clicks = 0),
                        html.Br(),
                        html.Br(), 
                        html.P('The custom rank groups you have saved for this session', style={'fontWeight':'bold'}),
                        html.Div(id='cust_rank_groups')])])
        
    ])

])

