import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
from data_parser import DataParser

data_parser = DataParser()

layout2 = html.Div([
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
                            'The number of requested latent topics to be extracted from the training corpus.',
                            target="tooltip-topics",
                        ),
                        # Dash Input component for setting the number of topics
                        dcc.Input( 
                            id='num-topics',
                            type='number',
                            value=5
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
                        'Maximum number of iterations through the corpus when inferring the topic distribution of a corpus.',
                        target="tooltip-iterations",
                    ),
                    # Dash Input component for setting the number of iterations used in the LDA model training
                    dcc.Input( 
                            id='num-iter',
                            type='number',
                            value=50
                    )
                ]
            ),
            html.Br(),
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
                    html.Div(id='slider-output')
                ]
            )
        ]
    ),
    html.Br(),
    # Button that initiates model training with the given variables
    html.Button('Train model', id='button', n_clicks = 0),
    html.Br(),
    # Loading-element wraps the LDA model visualisations
    dcc.Loading(
        id="loading",
        type="circle",
        fullscreen = True,
        children=[
            html.Details([
                html.Summary('20 top words from each topic'),
                # Table-element that shows the top topics from the trained model
                dash_table.DataTable(id="top-topics", 
                                    data=[],
                                    fixed_rows={'headers': True},
                                    style_table={'height': 300, 'overflowX': 'auto'}
                )
            ]),
            html.Details([
                html.Summary('Most representative letters for each topic'),
                # Table-element that shows the most representative letters for each topic
                dash_table.DataTable(id="letter-topics", 
                                    data=[]
                )
            ]),
            html.Details([
                html.Summary('Topic distribution across selected letters'),
                # Table-element that shows the topic distribution across letters
                dash_table.DataTable(id="letters-per-topic", 
                                    data=[]
                )
            ]),
            html.Details([
                html.Summary('Topic model visualisation'),
                # Iframe-element is used to serve the pyLDAvis visualization in html form
                html.Iframe(id='pyldavis-vis',
                            style=dict(position="absolute", width="100%", height="100%"))
            ])
        ]
    )
])
    
