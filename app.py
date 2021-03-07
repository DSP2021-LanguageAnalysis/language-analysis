# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_auth
import dash_table
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from dash import no_update
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
from data_parser import DataParser
from topic_model import prepare_data, filter_by_tag, train_lda, filter_by_sex, filter_by_rank
import pyLDAvis
import pyLDAvis.gensim
from pos_tab import PosTab

# Keep this out of source code repository - save in a file or a database
# Here just to demonstrate this authentication possibility
VALID_USERNAME_PASSWORD_PAIRS = {
    'user': 'user'
}

external_stylesheets = [
        #'https://codepen.io/chriddyp/pen/bWLwgP.css'
        dbc.themes.FLATLY
    ]


# Create the app, figures and define layout
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

pos_tab = PosTab()

# Parse letters to a Pandas DataFrame
data_parser = DataParser()
df = data_parser.letters_to_df()

def create_dataframes():

    # Word count DataFrame
    word_counts = df.groupby(['ID', 'Year']).size().to_frame(name = 'WordCount').reset_index()

    # POS counts for each letter
    pos_counts = df.groupby(['ID', 'Tags', 'Year', 'WordCount']).size().to_frame(name = 'PosCount').reset_index()
    pos_counts['PosCountNorm'] = pos_counts['PosCount']/pos_counts['WordCount']*100

    # Male/female noun ratio per year group
    nn1_MF = df.groupby(['ID', 'Tags', 'Year', 'WordCount', 'SenderSex']).size().to_frame(name = 'SenderSexCount').reset_index()
    nn1_MF['PosCountNorm'] = pos_counts['PosCount']/pos_counts['WordCount']
    nn1_MF = nn1_MF[nn1_MF['Tags'] == 'NN1']
    nn1_MF = nn1_MF.groupby(['Year', 'SenderSex']).mean().reset_index()
    nn1_MF = nn1_MF.drop(['WordCount','SenderSexCount'], axis=1)
    #app.logger.info(nn1_MF)
    
    # Male/female noun ratio per tag
    tag_MF = df.groupby(['ID', 'Tags', 'Year', 'WordCount', 'SenderSex']).size().to_frame(name = 'SenderSexCount').reset_index()
    tag_MF['PosCountNorm'] = pos_counts['PosCount']/pos_counts['WordCount']*100

    # NN1 tag count per year
    nn1_counts = pos_counts[pos_counts['Tags'] == 'NN1']
    nn1_counts = nn1_counts.groupby(['Year']).mean().reset_index()

    pos_set = set(df['Tags'])
    pos_list = [{'label':tag, 'value':tag} for tag in pos_set]

    rank_set = set(df['SenderRank'])
    rank_list = [{'label':rank, 'value':rank} for rank in rank_set]

    return word_counts, pos_counts, nn1_counts, pos_list, rank_set, rank_list, nn1_MF, tag_MF

word_counts, pos_counts, nn1_counts, pos_list, rank_set, rank_list, nn1_MF, tag_MF = create_dataframes()

wc_fig = px.scatter(word_counts, x="Year", y="WordCount", title='Word count for each letter in corpus')
fm_fig = px.bar(nn1_MF, x="Year", y="PosCountNorm", color='SenderSex', barmode='group')
#pc_fig = px.line(nn1_counts, x="Year", y="PosCountNorm")

app.layout = html.Div([
    html.Nav(
        className ='navbar navbar-expand-lg navbar-dark bg-primary', 
        children=[
            html.H1(className='navbar-brand', children='Data Science Project: Language variation')]) 
    , dcc.Tabs([
        dcc.Tab(label='POS tag visualisation', children=[
            dcc.Tabs([
                dcc.Tab(label='Scatter', children=[
                    # Simple word count graph    
                    html.Div(
                        children=[
                            dcc.Graph(
                                id='word-count-graph',
                                figure=wc_fig
                            )])])
                , dcc.Tab(label='Bar', children=[
                    # POS NN1 F/M
                    html.Div(
                        children=[
                            dcc.Graph(id='M/F_barChart',)
                            , dcc.Dropdown(
                                id='F/M_dropdown_1',
                                options=pos_list,
                                value=['NN1'],
                                multi=True
                            )])

                    # POS NN1 F/M with year grouping
                    , html.Div(
                        children=[
                            dcc.Graph(id='m-f-graph-year-grouping')
                            , "Select the number of year groups"
                            , html.Br()
                            , dcc.Input(
                                id="year-group-number", 
                                type="number", 
                                placeholder="input number of groups",
                                value=10
                            )])

                    # Dynamic attribute selection
                    , html.Div(
                        children=[
                            dcc.Graph(id='dynamic-attribute-bar')
                            , "Select the number of year groups"
                            , html.Br()
                            , dcc.Input(
                                id="pos-year-group-number", 
                                type="number", 
                                placeholder="input number of groups",
                                value=10
                            )
                            , html.Br() 
                            , "Select an attribute"
                            , dcc.Dropdown(
                                id='dynamic-attribute-selection',
                                options=[
                                    {'label': 'SenderSex', 'value': 'SenderSex'},
                                    {'label': 'SenderRank', 'value': 'SenderRank'}
                                ],
                                value='SenderSex',
                                multi=False
                            )
                            , dcc.Dropdown(
                                id='dynamic-subattribute-selection',
                                options=[
                                    {'label': 'M', 'value': 'M'},
                                    {'label': 'F', 'value': 'F'}
                                ],
                                value=['M', 'F'],
                                multi=True
                            )
                            , html.Br() 
                            # Button that initiates model training with the given variables
                            , html.Button('Apply selection', id='pos_button', n_clicks = 0)])
                ])
                , dcc.Tab(label='Line', children=[
                    # POS amount per year
                    html.Div(
                        children=[
                            dcc.Graph(id='pos_graph')
                            , dcc.Dropdown(
                                id='pos_dropdown',
                                options=pos_list,
                                value=['NN1'],
                                multi=True
                            )])

                    # POS group comparison
                    , html.Div(
                        children=[
                            dcc.Graph(id='pos_groups_graph')
                            , html.P(children='Group 1')
                            , dcc.Dropdown(
                                id='pos_groups_dropdown_1',
                                options=pos_list,
                                value=['NN', 'NN1'],
                                multi=True
                            )  
                            , html.P(children='Group 2')
                            , dcc.Dropdown(
                                id='pos_groups_dropdown_2',
                                options=pos_list,
                                value=['VBR', 'VB'],
                                multi=True)
                            ])
                ])
            ])
        ]),
        # Tab for the topic model selection and visualisation
        dcc.Tab(label='Topic modeling', children=[
            html.Div(
                children=[
                    html.Br()
                    , html.H4(children='Create a topic model with LDA')
                    , html.Br()
                    , html.H5(children='Set model parameters')
                    , html.Br()
                    , html.Div(children=[
                        'Select the '
                        , html.Span(
                            'number of topics',
                            id="tooltip-topics",
                        style={"textDecoration": "underline", "cursor": "pointer"},
                        )
                        ,': '
                        , dbc.Tooltip(
                            'The number of requested latent topics to be extracted from the training corpus.',
                            target="tooltip-topics",
                        )
                        # Dash Input component for setting the number of topics
                        , dcc.Input( 
                            id='num-topics',
                            type='number',
                            value=5
                        )
                    ])
                    , html.Br()
                    , html.Div(children=[
                        'Select the '
                        , html.Span(
                            'number of iterations',
                            id="tooltip-iterations",
                            style={"textDecoration": "underline", "cursor": "pointer"},
                        )
                        ,': '
                        , dbc.Tooltip(
                            'Maximum number of iterations through the corpus when inferring the topic distribution of a corpus.',
                            target="tooltip-iterations",
                        )
                        # Dash Input component for setting the number of iterations used in the LDA model training
                        , dcc.Input( 
                            id='num-iter',
                            type='number',
                            value=50
                        )
                    ])
                    , html.Br()
                    , html.H5(children='Filter data by POS tags')
                    , html.Br()
                    , html.Div(children=[
                        # Dash Dropdown component for selecting the tags for filtering the data
                        dcc.Dropdown(
                            id='tags-filter',
                            options=pos_list,
                            value=['NN1'],
                            multi=True
                        )
                    ])
                    , html.Br()
                    , html.H5(children='Filter by metadata')
                    , html.Br()
                    , html.Div(children=[
                        'Select letters based on the sex of the sender: '
                        # Dash RadioItems component for selecting the sex of the sender 
                        # for filtering the data
                        , dcc.RadioItems(
                            id='gender-filter',
                            options=[
                                {'label': 'All', 'value': 'A'},
                                {'label': 'Women', 'value': 'F'},
                                {'label': 'Men', 'value': 'M'}
                            ],
                            value='A'
                        )
                    ])
                    , html.Br()
                    , html.Div(children=[ 
                        'Select letters based on the rank of the sender: ' 
                        # Dash Dropdown component for selecting the rank of the sender
                        , dcc.Dropdown(
                            id='rank-filter',
                            options=rank_list,
                            value=list(rank_set),
                            multi=True
                        )
                    ])
                ]
            )
            , html.Br()
            # Button that initiates model training with the given variables
            , html.Button('Train model', id='button', n_clicks = 0)
            , html.Br()
            # Loading-element wraps the LDA model visualisations
            , dcc.Loading(
                id="loading",
                type="circle",
                fullscreen = True,
                children=[
                    # Table-element that shows the top topics from the trained model
                    dash_table.DataTable(id="top-topics", data=[])
                    , html.Br()
                    # Iframe-element is used to serve the pyLDAvis visualization in html form
                    , html.Iframe(id='pyldavis-vis',
                        style=dict(position="absolute", width="100%", height="100%"))]
            )          
        ])
    ])
])

# Function that generates Dash table from Pandas dataframe
def generate_table(dataframe):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(len(dataframe))
        ])
    ])

# Callback function for the topic model tab
@app.callback(
    Output('top-topics', 'data'),
    Output('top-topics', 'columns'),
    Output('pyldavis-vis', 'srcDoc'),
    Input('button', 'n_clicks'), # Only pressing the button initiates the function
    State('num-topics', 'value'), # Parameters given by the user are saved in State
    State('num-iter', 'value'),
    State('tags-filter', 'value'),
    State('gender-filter', 'value'),
    State('rank-filter', 'value'))
def model_params(clicks, topics, iterations, tags, gender, rank):
    if clicks > 0:
        # Uses the functions imported from topic_model.py
        data = filter_by_tag(df, tags)
        if gender != 'A':
            data = filter_by_sex(data, gender)
        if len(rank) != len(rank_set):
            data = filter_by_rank(data, rank)
        # Data preprocessing for the LDA model 
        corpus, dictionary, docs = prepare_data(data)
        # Creates the LDA topic model
        model, top_topics = train_lda(corpus, dictionary, topics, iterations)

        # Loop that creates a dataframe from the LDA top topics list
        i=1
        topic_dict = {}
        for topic in top_topics:
            words = []
            scores = []
            for t in topic[0]:
                words.append(t[1])
                scores.append(t[0])
            topic_dict['Topic {}: words'.format(i)] =  words 
            topic_dict['Topic {}: scores'.format(i)] = scores            
            i += 1

        dataframe = pd.DataFrame(topic_dict)
        cols = [{"name": i, "id": i} for i in dataframe.columns]

        # Creates the pyLDAvis visualisation of the LDA model
        vis_data = pyLDAvis.gensim.prepare(model, corpus, dictionary)
        html_vis = pyLDAvis.prepared_data_to_html(vis_data, template_type='general')

        return dataframe.to_dict('records'), cols, html_vis

    else:
        return no_update, no_update, no_update         


@app.callback(Output('pos_graph', 'figure'), [Input('pos_dropdown', 'value')])

def display_pos_graphs(selected_values):
    if selected_values is None:
        raise PreventUpdate
    else:
        mask = pos_counts['Tags'].isin(selected_values)
        fig = px.line(
            data_frame=pos_counts[mask].groupby(['Tags', 'Year']).mean().reset_index(), 
            x="Year", 
            y="PosCountNorm", 
            range_y=[0,50],
            labels={
                'Year': 'Year', 
                'PosCountNorm':'%'},
            color='Tags',
            title='Percentage of POS per year')
        return fig


@app.callback(
    Output('pos_groups_graph', 'figure'), 
    [Input('pos_groups_dropdown_1', 'value'),
    Input('pos_groups_dropdown_2', 'value')])

def display_grouped_pos_graphs(values1, values2):
    if values1 is None and values2 is None:
        raise PreventUpdate
    else:
        fig = go.Figure()
        mask = pos_counts['Tags'].isin(values1)
        fig.add_scatter(
            x=pos_counts[mask].groupby(['Tags', 'Year']).mean().reset_index().groupby(['Year']).sum().reset_index()['Year'], 
            y=pos_counts[mask].groupby(['Tags', 'Year']).mean().reset_index().groupby(['Year']).sum().reset_index()['PosCountNorm'],
            name='Group 1')

        mask = pos_counts['Tags'].isin(values2)
        fig.add_scatter(
            x=pos_counts[mask].groupby(['Tags', 'Year']).mean().reset_index().groupby(['Year']).sum().reset_index()['Year'], 
            y=pos_counts[mask].groupby(['Tags', 'Year']).mean().reset_index().groupby(['Year']).sum().reset_index()['PosCountNorm'],
            name='Group 2')
        fig.update_layout(yaxis_range=[0,50], title='Build POS groups and compare')
        return fig


@app.callback(
    Output('m-f-graph-year-grouping', 'figure'), 
    [Input('year-group-number', 'value')])

def display_grouped_pos_graphs(value):
    if value is None:
        raise PreventUpdate
    else:
        bins = pd.interval_range(start=1700, end=1800, periods=value, closed='right')
        labels = list(bins.astype(str))
        df = nn1_MF.copy()
        df['Year'] = df['Year'].astype('int')
        df['YearGroup'] = pd.cut(df['Year'], bins=bins,include_lowest=True, labels=labels, precision=0)
        df['YearGroup'] = df['YearGroup'].astype("str")
        df = df.groupby(['YearGroup', 'SenderSex']).mean().reset_index()
        return px.bar(df, x="YearGroup", y="PosCountNorm", color='SenderSex', barmode='group', title='Dynamically group years')  

@app.callback(
    Output('M/F_barChart', 'figure'), [Input('F/M_dropdown_1', 'value')])

def display_multiple_tags_barchart(values):
    if values is None:
        raise PreventUpdate
    else:
        mask = tag_MF['Tags'].isin(values)
        fig= px.bar(
            # can choose only one tag at a time
            data_frame=tag_MF[mask].groupby(['Year', 'SenderSex']).mean().reset_index(),
            x='Year', 
            y='PosCountNorm',
            range_y=[0,30],
            labels={
                'Year': 'Year', 
                'PosCountNorm':'Percentage of Tag'},
            color='SenderSex',
            barmode='group',
            title='Compare male and female tags')
        return fig

@app.callback(
    Output('dynamic-subattribute-selection', 'value'),
    Output('dynamic-subattribute-selection', 'options'),
    Input('dynamic-attribute-selection', 'value')
)
def pos_selection(input1):
    if input1 is None:
        raise PreventUpdate
    else:
        value, options = pos_tab.selection(df, input1)
        return value, options

@app.callback(
    Output('dynamic-attribute-bar', 'figure'), 
    Input('pos_button', 'n_clicks'), # Only pressing the button initiates the function
    State('dynamic-attribute-selection', 'value'),
    State('dynamic-subattribute-selection', 'value'),
    State('pos-year-group-number', 'value'))
def pos_dynamic_attributes(clicks, input1, input2, period_count):
    fig = pos_tab.dynamic_attributes(df, pos_counts, input1, input2, period_count)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
