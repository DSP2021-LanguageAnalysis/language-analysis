import os
import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
import globals

data_parser = globals.data_parser

pos_list = data_parser.get_pos_list()

layout1 = html.Div([
    html.Nav(
        className ='navbar navbar-expand-lg navbar-dark bg-primary', 
        children=[
            html.H1(className='navbar-brand', children='Data Science Project: Language variation')]
    ),
    html.H2('POS tag visualisation'),
    dcc.Link('Topic model', href='/app/topicmodel'),
    dcc.Tab(children=[
        dcc.Tabs([
            dcc.Tab(label='Instructions',
                children=[
                    html.H2("User instructions"),
                    #dcc.Link('link to github with more detailed documentation', href='https://github.com/DSP2021-LanguageAnalysis/language-analysis'),
                    dcc.Markdown(''' 
                    - [link to github with more detailed documentation](https://github.com/DSP2021-LanguageAnalysis/language-analysis)
                    - Click **topic model** under **POS tag Visualisation** to move to topic model view
                    - Click either **line** or **bar** to find different graphs
                    - Hover mouse over chart to find more options
                        - Download plot as a png
                        - Zoom
                            - undo by douple clicking graph
                        - Pan
                        - Box select
                            - undo by douple clicking graph
                        - Lasso select
                            - undo by douple clicking graph
                        - Zoom in
                        - Zoom out
                        - **Autoscale**
                            - scales the y-axis
                        - Reset axes
                    ''')
                ]
            ),
            dcc.Tab(label='Line', 
                children=[
                    html.Div(
                        children=[
                            dcc.Graph(id='line_graph'),
                            "Select the number of year groups",
                            html.Br(),
                            dcc.Input(
                                id="year-group-number-line", 
                                type="number", 
                                placeholder="input number of groups",
                                value=10
                            ),
                            html.Hr(),
                            'Selections for line 1',
                            html.Br(),
                            dcc.Dropdown(
                                id='pos_groups_dropdown_1_main',
                                options=data_parser.list_to_dash_option_dict(list(data_parser.pos_categories.keys())), 
                                value=['nouns'],
                                multi=True
                            ),
                            dcc.Dropdown(
                                id='pos_groups_dropdown_1_sub',
                                options=data_parser.list_to_dash_option_dict(list(data_parser.pos_categories['nouns'].keys())), 
                                value=list(data_parser.pos_categories['nouns'].keys()),
                                multi=True
                            ),   
                            html.Br(),
                            'Selections for line 2',
                            html.Br(),
                            dcc.Dropdown(
                                id='pos_groups_dropdown_2_main',
                                options=data_parser.list_to_dash_option_dict(list(data_parser.pos_categories.keys())), 
                                value=['pronouns'],
                                multi=True
                            ),
                            dcc.Dropdown(
                                id='pos_groups_dropdown_2_sub',
                                options=data_parser.list_to_dash_option_dict(list(data_parser.pos_categories['pronouns'].keys())), 
                                value=list(data_parser.pos_categories['pronouns'].keys()),
                                multi=True
                            ),
                            html.Br(), 
                            html.Button('Apply selection', id='update_line_button', n_clicks = 0)
                        ]
                    )
                ]
            ),
            dcc.Tab(label='Bar', 
                children=[
                    # main bar chart
                    html.Div(
                        children=[
                            dcc.Graph(id='bar_chart'),
                            "Select the number of year groups",
                            html.Br(),
                            dcc.Input(
                                id="year-group-number-bar", 
                                type="number", 
                                placeholder="input number of groups",
                                value=10
                            ),
                            html.Hr(),
                            'Tag selection',
                            html.Br(),
                            dcc.Dropdown(
                                id='pos_groups_dropdown_bar1_main',
                                options=data_parser.list_to_dash_option_dict(list(data_parser.pos_categories.keys())), 
                                value=['nouns'],
                                multi=True
                            ),
                            dcc.Dropdown(
                                id='pos_groups_dropdown_bar1_sub',
                                options=data_parser.list_to_dash_option_dict(list(data_parser.pos_categories['nouns'].keys())), 
                                value=list(data_parser.pos_categories['nouns'].keys()),
                                multi=True
                            ),
                            html.Br(), 
                            html.Button('Apply selection', id='update_bar_button', n_clicks = 0)
                        ]
                    ),
                    # main bar chart
                    html.Div(
                        children=[
                            dcc.Graph(id='count_bar_chart'),
                            "Select the number of year groups",
                            html.Br(),
                            dcc.Input(
                                id="year-group-number-count", 
                                type="number", 
                                placeholder="input number of groups",
                                value=10
                            ),
                            html.Hr(),
                            'Tag selection',
                            html.Br(),
                            dcc.Dropdown(
                                id='pos_groups_dropdown_count_main',
                                options=data_parser.list_to_dash_option_dict(list(data_parser.pos_categories.keys())), 
                                value=['nouns'],
                                multi=True
                            ),
                            dcc.Dropdown(
                                id='pos_groups_dropdown_count_sub',
                                options=data_parser.list_to_dash_option_dict(list(data_parser.pos_categories['nouns'].keys())), 
                                value=list(data_parser.pos_categories['nouns'].keys()),
                                multi=True
                            ),
                            html.Br(), 
                            html.Button('Apply selection', id='update_count_button', n_clicks = 0)
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
            )
        ])
    ])
])
