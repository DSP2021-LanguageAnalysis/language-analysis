# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_auth
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
from data_parser import DataParser

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


def create_dataframes():
    # Parse letters to a Pandas DataFrame
    data_parser = DataParser()
    df = data_parser.letters_to_df()

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

    return word_counts, pos_counts, nn1_counts, pos_list, nn1_MF, tag_MF


word_counts, pos_counts, nn1_counts, pos_list, nn1_MF, tag_MF = create_dataframes()

wc_fig = px.scatter(word_counts, x="Year", y="WordCount", title='Word count for each letter in corpus')
fm_fig = px.bar(nn1_MF, x="Year", y="PosCountNorm", color='SenderSex', barmode='group')
#pc_fig = px.line(nn1_counts, x="Year", y="PosCountNorm")

app.layout = html.Div(
    dcc.Tabs([
        dcc.Tab(label='POS tag visualisation', children=[
        # We could possible divide the app into multiple tabs, then user could 
        # change the visible layout by clicking nav bar items. However, data should
        # most likely be stored outside the layout as otherwise changin tab will
        # result in data loss.
            html.Nav(
                className ='navbar navbar-expand-lg navbar-dark bg-primary', 
                children=[
                    html.H1(className='navbar-brand', children='Data Science Project: Language variation')
                    # , html.A('Tab1', className="nav-item nav-link", href='/apps/Tab1')
                    # , html.A('Tab2', className="nav-item nav-link", href='/apps/Tab2')
            ]) 

            # Simple word count graph    
            , html.Div(
                children=[
                    dcc.Graph(
                        id='word-count-graph',
                        figure=wc_fig
                    )])

            # POS NN1 F/M
            , html.Div(
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
                    dcc.Graph(
                        id='m-f-graph-year-grouping')
                    , html.P('Number of year groups:', style={'display': 'inline-block', 'width': '10%'})
                    , dcc.Input(
                        id="year-group-number", 
                        type="number", 
                        placeholder="input number of groups",
                        value=10,
                        style={'display': 'inline-block'}
                    )])

        

            # POS amount per year
            , html.Div(
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
                        multi=True
                    )
                ]
            )
        ]),
        dcc.Tab(label='Topic modeling', children=[
            html.Nav(
                className ='navbar navbar-expand-lg navbar-dark bg-primary', 
                children=[
                    html.H1(className='navbar-brand', children='Data Science Project: Language variation')
            ]) 
            , html.Br()
            , html.H4(children='Create a topic model with LDA')
        ])
    ])
)


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

if __name__ == '__main__':
    app.run_server(debug=True)
