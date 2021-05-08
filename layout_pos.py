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


def line_selection(i):
    return html.Details([
                html.Summary(f'Line {i}', style={'fontWeight':'bold'}),
                html.Div(
                    style={'padding': '20px'},
                    children=[
                        "Custom name",
                        dcc.Input(id=f"line_name_{i}", type="text", placeholder="Custom name for line", value=f'Line {i}'),
                        html.Br(),
                        "Sender sex",
                        dcc.Dropdown(
                            id=f'line_sex_{i}',
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
                            id=f'line_senderrank_main_{i}',
                            options=data_parser.list_to_dash_option_dict(list(data_parser.rank_categories.keys())), 
                            value='Bipartite',
                            multi=False
                        ),
                        dcc.Dropdown(
                            id=f'line_senderrank_sub_{i}',
                            options=data_parser.dict_to_dash_options_with_hover(data_parser.rank_categories['Bipartite']), 
                            value=list(data_parser.rank_categories['Bipartite'].keys()),
                            multi=True
                        ),   
                        html.Br(),
                        "Relationship",
                        dcc.Dropdown(
                            id=f'line_relationship_main_{i}',
                            options=data_parser.list_to_dash_option_dict(list(data_parser.relationship_categories.keys())), 
                            value='Fine-grained',
                            multi=False
                        ),
                        dcc.Dropdown(
                            id=f'line_relationship_sub_{i}',
                            options=data_parser.dict_to_dash_options_with_hover(data_parser.relationship_categories['Fine-grained']), 
                            value=list(data_parser.relationship_categories['Fine-grained'].keys()),
                            multi=True
                        ),   
                        html.Br(),
                        "POS-tags",
                        dcc.Dropdown(
                            id=f'pos_groups_dropdown_{i}_main',
                            options=data_parser.list_to_dash_option_dict(list(data_parser.pos_categories.keys())), 
                            value=['nouns'],
                            multi=True
                        ),
                        dcc.Dropdown(
                            id=f'pos_groups_dropdown_{i}_sub',
                            options=data_parser.list_to_dash_option_dict(data_parser.pos_categories['nouns']), 
                            value=data_parser.pos_categories['nouns'],
                            multi=True
                        ),
                        dcc.Store(id=f'line_store_{i}', storage_type='local')
                    ])])

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
    html.Div(id='dummy_div'),
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
                            - This part of the application is developed to help answer questions about how the proportion of different parts of speech varies over time. 
                            - You can select sender attributes to narrow down the set of people. You might for instance want to see if there is a difference in the development of pronoun usage between men and women.
                            - [Link to github with more detailed documentation](https://github.com/DSP2021-LanguageAnalysis/language-analysis)

                            ##### Line graph
                            - In line graph view, you can see how the proportion of selected POS tags changes over time.

                            ##### Bar graph
                            - The bar graph shows metadata for lines drawn in the line graph view.
                            
                            ##### POS tags
                            - [Link to Constituent Likelihood Automatic Word-tagging System (CLAWS7) tagset](http://ucrel.lancs.ac.uk/claws7tags.html)
                            - The ditto tags that are present in the corpus are included when the main tag is selected. 
                            I.e. if user selects to see tag NN1 then ditto tags NN121, NN122, NN131, NN132, NN133 are also included.
                            - Note: The tags NPM2 (plural month noun) and MCGE (genitive cardinal number, neutral for number) have been removed from selection, as they are not featured in this particular corpus. 
                            - Punctuation tags have been excluded from the analysis.

                            ##### Attributes
                            - Pre-made groupings of social ranks
                                - **Fine grained** - Royalty (R) , Nobility (N) , Gentry Upper (GU), Gentry Lower (GL, G), Clergy Upper (CU), Clergy Lower (CL), Professional (P), Merchant (M), Other (O)
                                - **Regular** - Royalty (R) , Nobility (N) , Gentry (GU, GL, G), Clergy (CU, CL), Professional (P), Merchant (M), Other (O)
                                - **Tripartite** - Upper (R, N, GU, GL, G, CU), Middle (CL, P, M), Lower (O)
                                - **Bipartite** - Gentry (R, N, GU, GL, G, CU), Non-Gentry (CL, P, M, O)
                            
                            ##### Tips
                            - Hover mouse over chart to find more options
                                - Download plot as a **svg** (**WORKS CURRENTLY ONLY IN CHROME**)
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
                                    dcc.Graph(id='line_graph',
                                              config = {
                                                'toImageButtonOptions': {
                                                'format': 'svg', # one of png, svg, jpeg, webp
                                                'filename': 'line_graph',
                                                'height': 750,
                                                'width': 2000,
                                                'scale': 1 
                                                }
                                              })
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
                            html.Div([
                                'Which lines are visible:',
                                dcc.Checklist(
                                    id='line_visibility',
                                    options=[
                                        {'label': ' Line 1', 'value': 1},
                                        {'label': ' Line 2', 'value': 2},
                                        {'label': ' Line 3', 'value': 3},
                                        {'label': ' Line 4', 'value': 4},
                                        {'label': ' Line 5', 'value': 5},
                                        {'label': ' Line 6', 'value': 6},
                                        {'label': ' Line 7', 'value': 7},
                                        {'label': ' Line 8', 'value': 8},
                                        {'label': ' Line 9', 'value': 9},
                                        {'label': ' Line 10', 'value': 10}
                                    ],
                                    value=[1],
                                    labelStyle={'display': 'inline-block', 'margin-right': '10px'}
                            )]),
                            html.Br(),
                            html.Button('Apply selection', id='update_line_button_1', n_clicks = 0),
                            html.Hr(),
                            html.Details([
                                html.Summary('Apply same POS tag selections for all lines', style={'fontWeight':'bold'}),
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
                            html.Details([
                                html.Summary('Apply same attribute selections for all lines', style={'fontWeight':'bold'}),
                                html.Div(children=[
                                    dcc.Checklist(
                                        id='inherit_attributes',
                                        options=[
                                            {'label': ' Use this selection for all lines', 'value': '1'},
                                        ],
                                        value=[],
                                        labelStyle={'display': 'inline-block', 'margin-right': '10px'}
                                    ),
                                    "Sender sex",
                                    dcc.Dropdown(
                                        id='line_sex_0',
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
                                        id='line_senderrank_main_0',
                                        options=data_parser.list_to_dash_option_dict(list(data_parser.rank_categories.keys())), 
                                        value='Bipartite',
                                        multi=False
                                    ),
                                    dcc.Dropdown(
                                        id='line_senderrank_sub_0',
                                        options=data_parser.dict_to_dash_options_with_hover(data_parser.rank_categories['Bipartite']), 
                                        value=list(data_parser.rank_categories['Bipartite'].keys()),
                                        multi=True
                                    ),   
                                    html.Br(),
                                    "Relationship",
                                    dcc.Dropdown(
                                        id='line_relationship_main_0',
                                        options=data_parser.list_to_dash_option_dict(list(data_parser.relationship_categories.keys())), 
                                        value='Fine-grained',
                                        multi=False
                                    ),
                                    dcc.Dropdown(
                                        id='line_relationship_sub_0',
                                        options=data_parser.dict_to_dash_options_with_hover(data_parser.relationship_categories['Fine-grained']), 
                                        value=list(data_parser.relationship_categories['Fine-grained'].keys()),
                                        multi=True
                                    )])]),
                            html.Hr(),

                            ## Selections for individual lines
                            
                            line_selection(1),
                            line_selection(2),
                            line_selection(3),
                            line_selection(4),
                            line_selection(5),
                            line_selection(6),
                            line_selection(7),
                            line_selection(8),
                            line_selection(9),
                            line_selection(10),
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
                            html.Div(id='bar_names', style={'display': 'none'}),
                            dcc.Loading(
                                id="pos-loading",
                                type="circle",
                                fullscreen = False,
                                style={'paddingTop': '15px'},
                                children=[
                                    dcc.Graph(id='count_bar_chart',
                                              config = {
                                                'toImageButtonOptions': {
                                                'format': 'svg', # one of png, svg, jpeg, webp
                                                'filename': 'Bar_graph',
                                                'height': 750,
                                                'width': 2000,
                                                'scale': 1 
                                                }
                                              })
                                ]
                            ),
                            dcc.Loading(html.A(
                                id='download_plot_pdf',
                                href='',
                                children=[html.Button("Download plot as pdf", id='pdf_button')],
                                target='_blank',
                                download="bar_graph.pdf"
                            )),
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
