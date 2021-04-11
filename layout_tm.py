import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_table
import pandas as pd
import globals

data_parser = globals.data_parser

layout2 = html.Div(
    style={'padding': '20px'},
    children=[
    html.Nav(
        className ='navbar navbar-expand-lg navbar-dark bg-primary', 
        children=[
            html.H1(className='navbar-brand', children='Data Science Project: Language variation')
        ]
    ),
    html.H2('Topic modeling'),
    dcc.Link('POS tag visualisation', href='/app/postags'),
    html.Div(
        children=[
            html.Br(),
            html.H4(children='Create a topic model with LDA'),
            html.Br(),
            html.H5(children='Set model parameters'),
            html.Br(),
            html.Div(
                children=[
                    'Select the ',
                    html.Span(
                        'number of topics',
                        id="tooltip-topics",
                        style={"textDecoration": "underline", "cursor": "pointer"},
                        ),
                        ': ',
                        # Tooltip component for providing additional information to the user
                        dbc.Tooltip(
                            'the number of requested latent topics to be extracted from the training corpus.',
                            target="tooltip-topics",
                        ),
                        # Dash Input component for setting the number of topics
                        dcc.Input( 
                            id='num-topics',
                            type='number',
                            value=5,
                            min=2
                        )
                ]
            ),
            html.Br(),
            html.Div(
                children=[
                    'Select the ',
                    html.Span(
                        'number of iterations',
                        id="tooltip-iterations",
                        style={"textDecoration": "underline", "cursor": "pointer"},
                    ),
                    ': ',
                    # Tooltip component for providing additional information to the user
                    dbc.Tooltip(
                        'maximum number of iterations through the corpus when inferring the topic distribution of a corpus.',
                        target="tooltip-iterations",
                    ),
                    # Dash Input component for setting the number of iterations used in the LDA model training
                    dcc.Input( 
                            id='num-iter',
                            type='number',
                            value=50,
                            min=10
                    )
                ]
            ),
            html.Br(),
            html.Details([
                html.Summary('Advanced parameters',
                            style={'fontWeight':'bold'}),
                # alpha and eta
                html.Div(
                children=[
                    'Select the ',
                    html.Span(
                        'alpha parameter',
                        id="tooltip-alpha",
                        style={"textDecoration": "underline", "cursor": "pointer"},
                    ),
                    ': ',
                    # Tooltip component, alpha
                    dbc.Tooltip(
                        'positive smoothing parameter for prior distribution over topic weights in each document',
                        target="tooltip-alpha",
                    ),
                    # Dash Input component for alpha
                    dcc.Input( 
                            id='alpha',
                            type='number',
                            value=0.5,
                            min=0
                    ),
                            daq.BooleanSwitch(
                            id='alpha_boolean',
                            on=False,
                            label='auto:' ,
                            style={'display': 'inline-block'}
                            ) ,
                ]
            ),
            html.Br(),
            ### ETA
            html.Div(
                children=[
                    'Select the ',
                    html.Span(
                        'eta parameter',
                        id="tooltip-eta",
                        style={"textDecoration": "underline", "cursor": "pointer"},
                    ),
                    ': ',
                    # Tooltip component, alpha
                    dbc.Tooltip(
                        'positive smoothing parameter for prior distribution over word weights in each topic',
                        target="tooltip-eta",
                    ),
                    # Dash Input component for alpha
                    dcc.Input( 
                            id='eta',
                            type='number',
                            value=0.5,
                            min=0
                    ),
                    daq.BooleanSwitch(
                            id='eta_boolean',
                            on=False,
                            label='auto:' ,
                            style={'display': 'inline-block'}
                    ),
                ]
            ),
            html.Br(),
            html.Div(
                children=[
                    'Set ',
                    html.Span(
                        'seed',
                        id="tooltip-seed",
                        style={"textDecoration": "underline", "cursor": "pointer"},
                    ),
                    ': ',
                    # Tooltip component, seed
                    dbc.Tooltip(
                        'LDA is non-deterministic – setting a seed makes results replicable',
                        target="tooltip-seed",
                    ),
                    # Dash Input component for seed
                    dcc.Input( 
                            id='userseed',
                            type='number',
                            value=135,
                            min=1
                    ),
                ]
            ),
                
            ]),
            html.Br(),
            ###
            ###



            
            html.H5('Filter data by POS tags'),
            html.Br(),
            html.Div(
                children=[
                    # Dash Dropdown component for selecting the tags for filtering the data
                    dcc.Dropdown(
                        id='tags-filter',
                        options = data_parser.get_pos_list(),
                        value=['NN1'],
                        multi=True
                    )
                ]
            ),
            html.Br(),
            html.Br(),
            html.H5('Filter out stopwords'),
            html.Br(),
            html.Div(
                children=[
                    # Dash Dropdown component for manual stopword removal
                    dcc.Dropdown(
                        id='stopwords-filter',
                        options = data_parser.get_word_list(),
                        value=['letter'],
                        multi=True
                    )
                ]
            ),
            html.Br(),
            html.Br(),
            html.H5('Filter extremes'),
            html.Br(),
            html.Div(
                children=[
                    'Filter tokens appearing in less than selected',
                    html.Span(
                        'number of documents',
                        id="tooltip-extreme-low",
                        style={"textDecoration": "underline", "cursor": "pointer"},
                        ),
                        ': ',
                        # Tooltip component for providing additional information to the user
                        dbc.Tooltip(
                            'Tokens that feature in less than the selected number of documents will not be considered in the model',
                            target="tooltip-extreme-low",
                        ),
                        # Dash Input component for setting the number of topics
                        dcc.Input( 
                            id='filter-low',
                            type='number',
                            value=10,
                            min=0
                        )
                ]
            ),
            html.Br(),
            html.Div(
                children=[
                    'Filter tokens appearing in more than selected',
                    html.Span(
                        'proportion of documents',
                        id="tooltip-extreme-high",
                        style={"textDecoration": "underline", "cursor": "pointer"},
                        ),
                        ': ',
                        # Tooltip component for providing additional information to the user
                        dbc.Tooltip(
                            'Tokens that feature in more than the selected proportion of documents will not be considered in the model',
                            target="tooltip-extreme-high",
                        ),
                        # Dash Input component for setting the number of topics
                        dcc.Input( 
                            id='filter-high',
                            type='number',
                            value=50,
                            min=1
                        )
                ]
            ),
            html.Br(),
            html.H5('Filter by metadata'),
            html.Br(),
            html.Div(
                children=[
                    'Select letters based on the sex of the sender: ',
                    # Dash RadioItems component for selecting the sex of the sender 
                    # for filtering the data
                    dcc.RadioItems(
                        id='gender-filter',
                        options=[
                            {'label': 'All', 'value': 'A'},
                            {'label': 'Women', 'value': 'F'},
                            {'label': 'Men', 'value': 'M'}
                        ],
                        value='A'
                    )
                ]
            ),
            html.Br(),
            html.Div(
                children=[ 
                    'Select letters based on the rank of the sender: ', 
                    # Dash Dropdown component for selecting the rank of the sender
                    dcc.Dropdown(
                        id = 'rank-filter',
                        options = data_parser.get_rank()[1],
                        value = list(data_parser.get_rank()[0]),
                        multi = True
                    )
                ]
            ),
            html.Br(),
            html.Div(
                children=[ 
                    'Select letters based on the relationship between sender and recipient: ', 
                    # Dash Dropdown component for selecting the relationship tag for filtering the data
                    dcc.Dropdown(
                        id = 'rel-filter',
                        options = data_parser.get_relationship()[1],
                        value = list(data_parser.get_relationship()[0]),
                        multi = True
                    )
                ]
            ),
            html.Br(),
            html.Div(
                children=[ 
                    'Select time range for the letters to be used in the model: ', 
                    # Dash Slider component for selecting the time range
                    dcc.RangeSlider(
                        id='time-slider',
                        min=min(data_parser.get_years()),
                        max=max(data_parser.get_years()),
                        step=1,
                        value=[min(data_parser.get_years()), max(data_parser.get_years())]
                    ),
                    html.Div(id='slider-output'),
                    # Hidden div-element 
                    html.Div(id='slider-values', hidden=True)
                ]
            )
        ]
    ),
    html.Br(),
    # Button that initiates model training with the given variables
    html.Button('Train model', 
                id='button', 
                n_clicks = 0),
    html.Br(),
    # Loading-element wraps the LDA model visualisations
    dcc.Loading(
        id="loading",
        type="circle",
        fullscreen = True,
        style={'paddingTop': '15px'},
        children=[
            html.Div(
                id='tm-results',
                hidden=True,
                children=[
                    html.Details(
                        style={'paddingTop': '15px'},
                        children=[
                            html.Summary('20 top words from each topic',
                                        style={'fontWeight':'bold'}),
                            # Table-element that shows the top topics from the trained model
                            dash_table.DataTable(id="top-topics", 
                                                data=[],
                                                fixed_rows={'headers': True},
                                                style_table={'height': 300, 'overflowX': 'auto'}
                            )
                    ]),
                    html.Details(
                        style={'paddingTop': '15px'},
                        children=[
                            html.Summary('Most representative letters for selected topic',
                                    style={'fontWeight':'bold'}),
                            dcc.Dropdown(id="topic-selector", 
                                        persistence=False),
                            # Table-element that shows the most representative letters for each topic
                            dash_table.DataTable(id="letter-topics", 
                                                data=[]
                            )
                        ]
                    ),
                    html.Details(
                        style={'paddingTop': '15px'},
                        children=[
                            html.Summary('Topic distribution across selected letters',
                                        style={'fontWeight':'bold'}),
                            # Table-element that shows the topic distribution across letters
                            dash_table.DataTable(id="letters-per-topic", 
                                                data=[],
                            )
                    ]),
                    html.Details(
                        style={'paddingTop': '15px'},
                        children=[
                            html.Summary('Topic distribution in individual letters',
                                        style={'fontWeight':'bold'}),
                            dcc.Dropdown(id="letter-list", 
                                        multi=True,
                                        persistence=False),
                            html.Button('Get topics', 
                                        id='button2', 
                                        n_clicks = 0), 
                            dash_table.DataTable(id="letter-scores", 
                                                data=[]
                            )
                    ]),
                    html.Details(
                        style={'paddingTop': '15px'},
                        children=[
                            html.Summary('Topic model visualisation',
                                        style={'fontWeight':'bold'}),
                            # Iframe-element is used to serve the pyLDAvis visualization in html form
                            html.Iframe(id='pyldavis-vis',
                                        style=dict(position="absolute", width="100%", height="100%"))
                        ], 
                        open='open')
                ]
            )
        ]
    )
])
    
