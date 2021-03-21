import os
import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
#from data_parser import DataParser
from df_parser import DataParser

data_parser = DataParser()
#wc_fig = data_parser.get_wc_fig()
#pos_list = data_parser.get_pos_list()

layout1 = html.Div([
    html.Nav(
        className ='navbar navbar-expand-lg navbar-dark bg-primary', 
        children=[
            html.H1(className='navbar-brand', children='Data Science Project: Language variation')
            ,dcc.Link('Upload data', href='/app/upload')
            ,dcc.Link('POS tag visualisation', href='/app/postags')
            ,dcc.Link('Topic model', href='/app/topicmodel')
            ])
    , dcc.Tab(children=[
        dcc.Tabs([
            # dcc.Tab(label='Scatter', 
            #     children=[
            #         # Simple word count graph    
            #         html.Div(
            #             children=[
            #                 dcc.Graph(
            #                     id='word-count-graph',
            #                     #figure=wc_fig 
            #                 )
            #             ]
            #         )
            #     ]
            # ),
            dcc.Tab(label='Bar', 
                children=[
                    # POS NN1 F/M
                    html.Div(
                        children=[
                            dcc.Graph(id='M/F_barChart'),
                            dcc.Dropdown(
                                id='F/M_dropdown_1',
                                #options=pos_list, 
                                value=['NN1'],
                                multi=True
                            )
                        ]
                    ),
                    # POS NN1 F/M with year grouping
                    html.Div(
                        children=[
                            dcc.Graph(id='m-f-graph-year-grouping'),
                            "Select the number of year groups",
                            html.Br(),
                            dcc.Input(
                                id="year-group-number", 
                                type="number", 
                                placeholder="input number of groups",
                                value=10
                            )
                        ]
                    ),
                    # Dynamic attribute selection
                    html.Div(
                        children=[
                            dcc.Graph(id='dynamic-attribute-bar'),
                            "Select the number of year groups",
                            html.Br(),
                            dcc.Input(
                                id="pos-year-group-number", 
                                type="number", 
                                placeholder="input number of groups",
                                value=10
                            ),
                            html.Br(), 
                            "Select an attribute",
                            dcc.Dropdown(
                                id='dynamic-attribute-selection',
                                options=[
                                    {'label': 'SenderSex', 'value': 'SenderSex'},
                                    {'label': 'SenderRank', 'value': 'SenderRank'}
                                ],
                                value='SenderSex',
                                multi=False
                            ),
                            dcc.Dropdown(
                                id='dynamic-subattribute-selection',
                                options=[
                                    {'label': 'M', 'value': 'M'},
                                    {'label': 'F', 'value': 'F'}
                                ],
                                value=['M', 'F'],
                                multi=True
                            ),
                            html.Br(), 
                            html.Button('Apply selection', id='pos_button', n_clicks = 0)])
                ]
            ),
            dcc.Tab(label='Line', 
                children=[
                    # POS amount per year
                    html.Div(
                        children=[
                            dcc.Graph(id='pos_graph'),
                            dcc.Dropdown(
                                id='pos_dropdown',
                                #options=pos_list, 
                                value=['NN1'],
                                multi=True
                            )
                        ]
                    ),
                    # POS group comparison
                    html.Div(
                        children=[
                            dcc.Graph(id='pos_groups_graph'),
                            html.P(children='Group 1'),
                                dcc.Dropdown(
                                    id='pos_groups_dropdown_1',
                                    #options=pos_list, 
                                    value=['NN', 'NN1'],
                                    multi=True
                                ),  
                                html.P(children='Group 2'),
                                dcc.Dropdown(
                                    id='pos_groups_dropdown_2',
                                    #options=pos_list, 
                                    value=['VBR', 'VB'],
                                    multi=True)
                        ]
                    )
                ]
            )
        ])
    ])
])
