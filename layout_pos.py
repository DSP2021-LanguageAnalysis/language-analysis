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
            dbc.NavItem(dbc.NavLink('Overview', href='/app/overview')),
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
                            #html.H2("User instructions"),
                            #dcc.Link('link to github with more detailed documentation', href='https://github.com/DSP2021-LanguageAnalysis/language-analysis'),
                            dcc.Markdown(''' 
                            ##### General
                            - This part of the application is developed to help answer question about how usage of POS tags varies over time. 
                            - You can select sender attributes to narrow down the set of people. 
                            You might for instance want to see if there is a difference in the development of pronoun usage between men and women.
                            - [Link to github with more detailed documentation](https://github.com/DSP2021-LanguageAnalysis/language-analysis)

                            ##### Line graph
                            - In line graph view, you can see how the amount of selected POS tags changes over time.

                            ##### Bar graph
                            - The bar graph shows metadata for lines drawn in the line graph view.
                            
                            ##### POS tags
                            - [Link to Constituent Likelihood Automatic Word-tagging System (CLAWS7) tagset](http://ucrel.lancs.ac.uk/claws7tags.html)
                            - The ditto tags that are present in the corpus are included when the main tag is selected. 
                            I.e. if user selects to see tag NN1 then ditto tags NN121, NN122, NN131, NN132, NN133 are also included.
                            - Note: The tags NPM2 (plural month noun) and MCGE (genitive cardinal number, neutral for number) have been removed from selection, as they are not featured in this particular corpus. 

                            ##### Attributes
                            - Pre-Made Class Grouping Classifications
                                - **Fine grained** - Royalty (R) , Nobility (N) , Gentry Upper (GU), Gentry Lower (GL, G), Clergy Upper (CU), Clergy Lower (CL), Professional (P), Merchant (M), Other (O)
                                - **Regular** - Royalty (R) , Nobility (N) , Gentry (GU, GL, G), Clergy (CU, CL), Professional (P), Merchant (M), Other (O)
                                - **Tripartite** - Upper (R, N, GU, GL, G, CU), Middle (CL, P, M), Lower (O)
                                - **Bipartite** - Gentry (R, N, GU, GL, G, CU), Non-Gentry (CL, P, M, O)
                            
                            ##### Tips
                            - Hover mouse over chart to find more options
                                - Download plot as a png
                                - Zoom
                                    - undo by double clicking graph
                                - Pan
                                - Box select
                                    - undo by double clicking graph
                                - Lasso select
                                    - undo by double clicking graph
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
                            dcc.Loading(
                                id="pos-loading",
                                type="circle",
                                fullscreen = False,
                                style={'paddingTop': '15px'},
                                children=[
                                    dcc.Graph(id='line_graph')
                                ]
                            ),
                            'Select time range:', 
                            # Dash Slider component for selecting the time range
                            dcc.RangeSlider(
                                id='line_time_slider',
                                min=min(data_parser.get_years()),
                                max=max(data_parser.get_years()),
                                step=1,
                                value=[1680, 1800],
                                updatemode='drag'
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
                                        options=data_parser.list_to_dash_option_dict(data_parser.pos_categories['nouns']), 
                                        value=data_parser.pos_categories['nouns'],
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
                                        options=data_parser.list_to_dash_option_dict(data_parser.pos_categories['nouns']), 
                                        value=data_parser.pos_categories['nouns'],
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
                                        options=data_parser.list_to_dash_option_dict(data_parser.pos_categories['pronouns']), 
                                        value=data_parser.pos_categories['pronouns'],
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
                                        options=data_parser.list_to_dash_option_dict(data_parser.pos_categories['verbs']), 
                                        value=data_parser.pos_categories['verbs'],
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
                    
                    # word count bar chart
                    html.Div(
                        style={'padding': '20px'},
                        children=[
                            html.Div(id='bar_df', style={'display': 'none'}),
                            dcc.Loading(
                                id="pos-loading",
                                type="circle",
                                fullscreen = False,
                                style={'paddingTop': '15px'},
                                children=[
                                    dcc.Graph(id='count_bar_chart')
                                ]
                            ),
                            html.Div(id='size_info',
                                     style={'paddingBottom': '20px'}),
                            'Show the number of ',
                            dcc.RadioItems(
                                id='bar_what_count',
                                options=[
                                    {'label': ' Words', 'value': 'words'},
                                    {'label': ' Letters', 'value': 'letters'},
                                    {'label': ' People', 'value': 'people'}
                                ],
                                value='words',
                                labelStyle={'display': 'inline-block', 'margin-right': '10px'}
                            ),
                            'Group the bars by ',
                            dcc.RadioItems(
                                id='bar_groub_by',
                                options=[
                                    {'label': ' Sender\'s sex', 'value': 'SenderSex'},
                                    {'label': ' Sender\'s rank', 'value': 'SenderRank'},
                                    {'label': ' Sender\'s relationship with recipient', 'value': 'RelCode'}
                                ],
                                value='SenderSex',
                                labelStyle={'display': 'inline-block', 'margin-right': '10px'}
                            )
                        ]
                    ),
                ]
            )
    ])
])
