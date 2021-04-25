import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_table
import pandas as pd
import globals

data_parser = globals.data_parser

layout2 = html.Div(
    #style={'padding': '20px'},
    children=[
    dcc.ConfirmDialog(
        id='confirm',
        message='Topic model received no data for training. Please try other filtering options.',
    ),
    dbc.Nav(
        className ='navbar navbar-expand-lg navbar-dark bg-primary', 
        children=[
            html.H1(className='navbar-brand', children='VARIENG: TCEECE corpus analysis'),
            dbc.NavItem(dbc.NavLink('Overview', href='/app/overview')),
            dbc.NavItem(dbc.NavLink('POS tag analysis', href='/app/postags')),
            dbc.NavItem(dbc.NavLink('Topic model', active=True, href='/app/topicmodel')),
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
                        #dcc.Link('Link to github with more detailed documentation', href='https://github.com/DSP2021-LanguageAnalysis/language-analysis'),
                        dcc.Markdown('''
                        ##### General
                        - This part of the application is for exploring the dominant topics in the corpus. 
                        - [Link to github with more detailed documentation](https://github.com/DSP2021-LanguageAnalysis/language-analysis)
                        - [Link to Constituent Likelihood Automatic Word-tagging System (CLAWS7) tagset](http://ucrel.lancs.ac.uk/claws7tags.html)
                        
                        #### Parametrisation and Filtration
                        - Select the model parameters
                            - Choose the number of topics to be generated
                            - Choose the number of iterations to be completed by the model
                        - Select **Advanced parameters** to view more options (detail given in documentation)
                        - Select filtration parameters - Filter corpus by:
                            - POS tagged tokens
                                - [Link to Constituent Likelihood Automatic Word-tagging System (CLAWS7) tagset](http://ucrel.lancs.ac.uk/claws7tags.html)
                                - The ditto tags that are present in the corpus are included when the main tag is selected. 
                                  I.e. if user selects to see tag NN1 then ditto tags NN121, NN122, NN131, NN132, NN133 are also included.
                                - Note: The tags NPM2 (plural month noun) and MCGE (genitive cardinal number, neutral for number) have been removed from selection, as they are not featured in this particular corpus.       
                            - Custom stopword list
                            - "Extreme" distributed tokens
                            - Sex of sender
                            - Rank of sender
                                - Pre-made groupings of social ranks
                                - **Fine grained** - Royalty (R) , Nobility (N) , Gentry Upper (GU), Gentry Lower (GL, G), Clergy Upper (CU), Clergy Lower (CL), Professional (P), Merchant (M), Other (O)
                                - **Regular** - Royalty (R) , Nobility (N) , Gentry (GU, GL, G), Clergy (CU, CL), Professional (P), Merchant (M), Other (O)
                                - **Tripartite** - Upper (R, N, GU, GL, G, CU), Middle (CL, P, M), Lower (O)
                                - **Bipartite** - Gentry (R, N, GU, GL, G, CU), Non-Gentry (CL, P, M, O)
                            - Relationship between sender and recipient
                            - Time period during which the letter was sent
                            
                        #### Create Model
                        - Click **Train model** to generate results and visualisation
                            - With default options, the algorithm takes approximately 30 seconds to generate results
                            - Changes in parameters will alter this waiting time
                            
                        #### Results
                        - Select dropdown menus to reveal different results: 
                            - View top 20 words from each topic
                            - Most represented letters from each topic
                                - Select topic and view the letters which most contribute to it
                            - View topic distribution over each letter
                            - View topic distribution in individual letters
                                - Select letter and view its contribution to each individual topic
                            - View topic visualisation
                                - Scroll over topic in intertopic distance map to view its most relevant tokens 
                                - Adjust relevance metric with slider (detail in documentation)
                            ''')
                        ])
                ]
            ),
        dcc.Tab(
            label='Topic Model',
            children=[
                html.Div(
                    style={'padding': '20px'},
                    children=[
                        html.Br(),
                        html.H4(children='Create a topic model with Latent Dirichlet Allocation (LDA)'),
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
                                        min=2,
                                        persistence=True
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
                                        min=10,
                                        persistence=True
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
                                        min=0,
                                        persistence=True
                                ),
                                        daq.BooleanSwitch(
                                        id='alpha_boolean',
                                        on=False,
                                        persistence=True,
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
                                # Tooltip component, eta
                                dbc.Tooltip(
                                    'Positive smoothing parameter for prior distribution over word weights in each topic',
                                    target="tooltip-eta",
                                ),
                                # Dash Input component for eta
                                dcc.Input( 
                                        id='eta',
                                        type='number',
                                        value=0.5,
                                        min=0,
                                        persistence=True
                                ),
                                daq.BooleanSwitch(
                                        id='eta_boolean',
                                        on=False,
                                        persistence=True,
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
                                    min=1,
                                    persistence=True
                                ),
                            ]
                        ),
                        ]),
                        html.Br(),            
                        html.H5('Filter data by POS tags'),
                        html.Br(),
                        dcc.Dropdown(
                            id='pos_tm_main',
                            options=data_parser.list_to_dash_option_dict(list(data_parser.pos_categories.keys())), 
                            value=['nouns'],
                            multi=True,
                            persistence=True
                        ),
                        dcc.Dropdown(
                            id='pos_tm_sub',
                            options=data_parser.list_to_dash_option_dict(data_parser.pos_categories['nouns']), 
                            value=data_parser.pos_categories['nouns'],
                            multi=True
                        ), 
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
                                    multi=True,
                                    persistence=True
                                )
                            ]
                        ),
                        html.Br(),
                        html.Br(),
                        html.H5('Filter extremes'),
                        html.Br(),
                        html.Div(
                            children=[
                                'Filter tokens appearing in less than selected ',
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
                                    value=0,
                                    min=0,
                                    persistence=True
                                )
                            ]
                        ),
                        html.Br(),
                        html.Div(
                            children=[
                            'Filter tokens appearing in more than selected ',
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
                                    value=1,
                                    min=0.01,
                                    max=1,
                                    step=0.01,
                                    persistence=True
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
                                    value='A',
                                    labelStyle={'display': 'inline-block'},
                                    persistence=True
                                )
                            ]
                        ),
                        html.Br(),
                        html.Div(
                            children=[ 
                                'Select letters based on the rank of the sender: ', 
                                # Dash Dropdown component for selecting the rank of the sender
                                dcc.Dropdown(
                                    id='rank-main',
                                    options=data_parser.list_to_dash_option_dict(list(data_parser.rank_categories.keys())), 
                                    value='Bipartite',
                                    multi=False
                                ),
                                dcc.Dropdown(
                                    id='rank-sub',
                                    options=data_parser.dict_to_dash_options_with_hover(data_parser.rank_categories['Bipartite']), 
                                    value=list(data_parser.rank_categories['Bipartite'].keys()),
                                    multi=True
                                ) 
                            ]
                        ),
                        html.Br(),
                        html.Div(
                            children=[ 
                                'Select letters based on the relationship between sender and recipient: ', 
                                # Dash Dropdown component for selecting the relationship tag for filtering the data
                                dcc.Dropdown(
                                    id='relationship-main',
                                    options=data_parser.list_to_dash_option_dict(list(data_parser.relationship_categories.keys())), 
                                    value='Fine-grained',
                                    multi=False
                                ),
                                dcc.Dropdown(
                                    id='relationship-sub',
                                    options=data_parser.dict_to_dash_options_with_hover(data_parser.relationship_categories['Fine-grained']), 
                                    value=list(data_parser.relationship_categories['Fine-grained'].keys()),
                                    multi=True
                                ),  
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
                                    value=[min(data_parser.get_years()), max(data_parser.get_years())],
                                    persistence=True,
                                    updatemode='drag'
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
                html.Div(
                    style={'padding': '20px'},
                    children=[
                        html.Button('Train model', 
                                    id='button', 
                                    n_clicks = 0)
                    ]
                ),
                html.Br(),
                # Loading-element wraps the LDA model visualisations
                dcc.Loading(
                    id="loading",
                    type="circle",
                    fullscreen = True,
                    style={'paddingTop': '15px'},
                    children=[
                            html.Div(id='corpus_size_info',
                                     style={'padding': '20px'}),
                            html.Br(),
                            html.Div(
                                style={'padding': '20px'},
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
                                                                data=[],
                                                                page_size=10
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
                                                                data=[]
                                                                
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
                    ]
                )
            ])
    ]
)
