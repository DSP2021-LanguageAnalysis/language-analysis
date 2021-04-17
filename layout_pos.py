import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
import globals

data_parser = globals.data_parser

pos_list = data_parser.get_pos_list()

layout1 = html.Div([
    dbc.Nav(
        className ='navbar navbar-expand-lg navbar-dark bg-primary', 
        children=[
            html.H1(className='navbar-brand', children='VARIENG: TCEECE corpus analysis'),
            dbc.NavItem(dbc.NavLink('POS tag analysis', active=True, href='/app/postags')),
            dbc.NavItem(dbc.NavLink('Topic model', href='/app/topicmodel')),
            dbc.NavItem(dbc.NavLink('Add custom groups', href='/app/customize'))
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
                        ])
                ]
            ),
            dcc.Tab(
                label='Line', 
                children=[
                    html.Div(
                        style={'padding': '20px'},
                        children=[
                            dcc.Graph(id='line_graph'),
                            'Select time range:', 
                            # Dash Slider component for selecting the time range
                            dcc.RangeSlider(
                                id='line_time_slider',
                                min=min(data_parser.get_years()),
                                max=max(data_parser.get_years()),
                                step=1,
                                value=[1680, 1800]
                            ),
                            html.Div(id='line_slider_output'),
                            # Hidden div-element 
                            html.Div(id='line_slider_values', hidden=True),
                            html.Div([
                            "Select period length for grouping",
                            dcc.Input(
                                id="line_period_length", 
                                type="number", 
                                placeholder="input period length",
                                value=20
                            )]),
                            html.Div([
                            "Set name for the graph",
                            dcc.Input(
                                id="line_graph_name", 
                                type="text", 
                                value=""
                            )]),
                            html.Button('Apply selection', id='update_line_button_1', n_clicks = 0),
                            html.Hr(),
                            html.Details([
                                html.Summary('Apply same selections for all lines', style={'fontWeight':'bold'}),
                                html.Div(children=[
                                    dcc.Checklist(
                                        id='inherit_pos',
                                        options=[
                                            {'label': ' Use this selection for all lines', 'value': '1'},
                                        ],
                                        value=[],
                                        labelStyle={'display': 'inline-block', 'margin-right': '10px'}
                                    ),
                                    dcc.Dropdown(
                                        id='pos_groups_dropdown_0_main',
                                        options=data_parser.list_to_dash_option_dict(list(data_parser.pos_categories.keys())), 
                                        value=['nouns'],
                                        multi=True
                                    ),
                                    dcc.Dropdown(
                                        id='pos_groups_dropdown_0_sub',
                                        options=data_parser.list_to_dash_option_dict(list(data_parser.pos_categories['nouns'].keys())), 
                                        value=list(data_parser.pos_categories['nouns'].keys()),
                                        multi=True
                                    )])]),
                            html.Hr(),
                            'Which lines are visible:',
                            html.Br(),
                            dcc.Checklist(
                                id='line_visibility',
                                options=[
                                    {'label': ' Line 1', 'value': '1'},
                                    {'label': ' Line 2', 'value': '2'},
                                    {'label': ' Line 3', 'value': '3'}
                                ],
                                value=['1'],
                                labelStyle={'display': 'inline-block', 'margin-right': '10px'}
                            ),
                            html.Br(),
                            ## Selections for group 1
                            html.Details(
                                open=True,
                                children=[
                                html.Summary('Line 1', style={'fontWeight':'bold'}),
                                html.Div(children=[
                                    "Custom name",
                                    dcc.Input(id="line_name_1", type="text", placeholder="Custom name for line", value='Line 1'),
                                    html.Br(),
                                    "Sender sex",
                                    dcc.Dropdown(
                                        id='line_sex_1',
                                        options=[
                                            {'label': 'M', 'value': 'M'},
                                            {'label': 'F', 'value': 'F'}
                                        ], 
                                        value=['M', 'F'],
                                        multi=True
                                    ),   
                                    html.Br(),
                                    "Sender rank",
                                    dcc.Dropdown(
                                        id='line_senderrank_main_1',
                                        options=data_parser.list_to_dash_option_dict(list(data_parser.rank_categories.keys())), 
                                        value='Bipartite',
                                        multi=False
                                    ),
                                    dcc.Dropdown(
                                        id='line_senderrank_sub_1',
                                        options=data_parser.dict_to_dash_options_with_hover(data_parser.rank_categories['Bipartite']), 
                                        value=list(data_parser.rank_categories['Bipartite'].keys()),
                                        multi=True
                                    ),   
                                    html.Br(),
                                    "Relationship",
                                    dcc.Dropdown(
                                        id='line_relationship_main_1',
                                        options=data_parser.list_to_dash_option_dict(list(data_parser.relationship_categories.keys())), 
                                        value='Fine-grained',
                                        multi=False
                                    ),
                                    dcc.Dropdown(
                                        id='line_relationship_sub_1',
                                        options=data_parser.dict_to_dash_options_with_hover(data_parser.relationship_categories['Fine-grained']), 
                                        value=list(data_parser.relationship_categories['Fine-grained'].keys()),
                                        multi=True
                                    ),   
                                    html.Br(),
                                    "POS-tags",
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
                                    ) 
                            ])]),
                            html.Details([
                                html.Summary('Line 2', style={'fontWeight':'bold'}),
                                html.Div(children=[
                                    "Custom name",
                                    dcc.Input(id="line_name_2", type="text", placeholder="Custom name for line", value='Line 2'),
                                    html.Br(),
                                    "Sender sex",
                                    dcc.Dropdown(
                                        id='line_sex_2',
                                        options=[
                                            {'label': 'M', 'value': 'M'},
                                            {'label': 'F', 'value': 'F'}
                                        ], 
                                        value=['M', 'F'],
                                        multi=True
                                    ),   
                                    html.Br(),
                                    "Sender rank",
                                    dcc.Dropdown(
                                        id='line_senderrank_main_2',
                                        options=data_parser.list_to_dash_option_dict(list(data_parser.rank_categories.keys())), 
                                        value='Bipartite',
                                        multi=False
                                    ),
                                    dcc.Dropdown(
                                        id='line_senderrank_sub_2',
                                        options=data_parser.dict_to_dash_options_with_hover(data_parser.rank_categories['Bipartite']), 
                                        value=list(data_parser.rank_categories['Bipartite'].keys()),
                                        multi=True
                                    ),   
                                    html.Br(),
                                    "Relationship",
                                    dcc.Dropdown(
                                        id='line_relationship_main_2',
                                        options=data_parser.list_to_dash_option_dict(list(data_parser.relationship_categories.keys())), 
                                        value='Fine-grained',
                                        multi=False
                                    ),
                                    dcc.Dropdown(
                                        id='line_relationship_sub_2',
                                        options=data_parser.dict_to_dash_options_with_hover(data_parser.relationship_categories['Fine-grained']), 
                                        value=list(data_parser.relationship_categories['Fine-grained'].keys()),
                                        multi=True
                                    ),   
                                    html.Br(),
                                    "POS-tags",
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
                                    ) 
                            ])]),
                            html.Details([
                                html.Summary('Line 3', style={'fontWeight':'bold'}),
                                html.Div(children=[
                                    "Custom name",
                                    dcc.Input(id="line_name_3", type="text", placeholder="Custom name for line", value='Line 3'),
                                    html.Br(),
                                    "Sender sex",
                                    dcc.Dropdown(
                                        id='line_sex_3',
                                        options=[
                                            {'label': 'M', 'value': 'M'},
                                            {'label': 'F', 'value': 'F'}
                                        ], 
                                        value=['M', 'F'],
                                        multi=True
                                    ),   
                                    html.Br(),
                                    "Sender rank",
                                    dcc.Dropdown(
                                        id='line_senderrank_main_3',
                                        options=data_parser.list_to_dash_option_dict(list(data_parser.rank_categories.keys())), 
                                        value='Bipartite',
                                        multi=False
                                    ),
                                    dcc.Dropdown(
                                        id='line_senderrank_sub_3',
                                        options=data_parser.dict_to_dash_options_with_hover(data_parser.rank_categories['Bipartite']), 
                                        value=list(data_parser.rank_categories['Bipartite'].keys()),
                                        multi=True
                                    ),   
                                    html.Br(),
                                    "Relationship",
                                    dcc.Dropdown(
                                        id='line_relationship_main_3',
                                        options=data_parser.list_to_dash_option_dict(list(data_parser.relationship_categories.keys())), 
                                        value='Fine-grained',
                                        multi=False
                                    ),
                                    dcc.Dropdown(
                                        id='line_relationship_sub_3',
                                        options=data_parser.dict_to_dash_options_with_hover(data_parser.relationship_categories['Fine-grained']), 
                                        value=list(data_parser.relationship_categories['Fine-grained'].keys()),
                                        multi=True
                                    ),   
                                    html.Br(),
                                    "POS-tags",
                                    dcc.Dropdown(
                                        id='pos_groups_dropdown_3_main',
                                        options=data_parser.list_to_dash_option_dict(list(data_parser.pos_categories.keys())), 
                                        value=['verbs'],
                                        multi=True
                                    ),
                                    dcc.Dropdown(
                                        id='pos_groups_dropdown_3_sub',
                                        options=data_parser.list_to_dash_option_dict(list(data_parser.pos_categories['verbs'].keys())), 
                                        value=list(data_parser.pos_categories['verbs'].keys()),
                                        multi=True
                                    ) 
                            ])]),
                            html.Br(), 
                            html.Button('Apply selection', id='update_line_button', n_clicks = 0)
                        ]
                    )
                ]
            ),
            dcc.Tab(
                label='Bar', 
                children=[
                    # main bar chart
                    html.Div(
                        style={'padding': '20px'},
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
                    # word count bar chart
                    html.Div(
                        children=[
                            dcc.Graph(id='count_bar_chart'),
                            # "Select the number of year groups",
                            # html.Br(),
                            # dcc.Input(
                            #     id="year-group-number-count", 
                            #     type="number", 
                            #     placeholder="input number of groups",
                            #     value=10
                            # ),
                            # html.Hr(),
                            # 'Tag selection',
                            # html.Br(),
                            # dcc.Dropdown(
                            #     id='pos_groups_dropdown_count_main',
                            #     options=data_parser.list_to_dash_option_dict(list(data_parser.pos_categories.keys())), 
                            #     value=['nouns'],
                            #     multi=True
                            # ),
                            # dcc.Dropdown(
                            #     id='pos_groups_dropdown_count_sub',
                            #     options=data_parser.list_to_dash_option_dict(list(data_parser.pos_categories['nouns'].keys())), 
                            #     value=list(data_parser.pos_categories['nouns'].keys()),
                            #     multi=True
                            # ),
                            # html.Br(), 
                            # html.Button('Apply selection', id='update_count_button', n_clicks = 0)
                        ]
                    ),
                    # Dynamic attribute selection
                    html.Div(
                        style={'padding': '20px'},
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
