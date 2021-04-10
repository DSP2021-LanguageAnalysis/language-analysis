import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

from app import app
from pos_tab import PosTab
import globals

data_parser = globals.data_parser

pos_tab = PosTab()
df = data_parser.df
pos_counts = data_parser.get_pos_counts()
nn1_MF = data_parser.get_mfn_ratio()
tag_MF = data_parser.get_mfn_tag()


@app.callback(
    Output('pos_groups_dropdown_1_sub', 'value'),
    Output('pos_groups_dropdown_1_sub', 'options'),
    [Input('pos_groups_dropdown_1_main', 'value')])
def line_group_1_options(mains):

    values = []
    options = []
    for main in mains:
        value = list(data_parser.pos_categories[main].keys())
        values.extend(value)
        options.extend(data_parser.list_to_dash_option_dict(value))

    return values, options

# line graph
@app.callback(
    Output('pos_groups_dropdown_2_sub', 'value'),
    Output('pos_groups_dropdown_2_sub', 'options'),
    [Input('pos_groups_dropdown_2_main', 'value')])
def line_group_2_options(mains):

    values = []
    options = []
    for main in mains:
        value = list(data_parser.pos_categories[main].keys())
        values.extend(value)
        options.extend(data_parser.list_to_dash_option_dict(value))
    
    return values, options


@app.callback(
    Output('line_graph', 'figure'), 
    Input('update_line_button', 'n_clicks'), # Only pressing the button initiates the function
    [State('pos_groups_dropdown_1_main', 'value')],
    [State('pos_groups_dropdown_1_sub', 'value')],
    [State('pos_groups_dropdown_2_main', 'value')],
    [State('pos_groups_dropdown_2_sub', 'value')],
    [State('year-group-number-line', 'value')])
def display_line_graph(n_clicks, values0, values1, values2, values3, periods):

    if n_clicks is not None:
        bins = pd.interval_range(start=1700, end=1800, periods=periods, closed='right')
        labels = list(bins.astype(str))

        df = data_parser.df
        df = df.groupby(['ID', 'SenderSex', 'SenderRank', 'RelCode', 'Tags', 'Year', 'WordCount']).size().to_frame(name = 'PosCount').reset_index()
        df['PosCountNorm'] = df['PosCount']/df['WordCount']*100
        
        df['Year'] = df['Year'].astype('int')
        df['YearGroup'] = pd.cut(df['Year'], bins=bins,include_lowest=True, labels=labels, precision=0)
        df['YearGroup'] = df['YearGroup'].astype("str")
        df = df.groupby(['YearGroup', 'Tags']).mean().reset_index()

        fig = go.Figure()
        mask = df['Tags'].isin(values1)
        fig.add_scatter(
            x=df[mask].groupby(['Tags', 'YearGroup']).mean().reset_index().groupby(['YearGroup']).sum().reset_index()['YearGroup'], 
            y=df[mask].groupby(['Tags', 'YearGroup']).mean().reset_index().groupby(['YearGroup']).sum().reset_index()['PosCountNorm'],
            name='Line 1')

        mask = pos_counts['Tags'].isin(values3)
        fig.add_scatter(
            x=df[mask].groupby(['Tags', 'YearGroup']).mean().reset_index().groupby(['YearGroup']).sum().reset_index()['YearGroup'], 
            y=df[mask].groupby(['Tags', 'YearGroup']).mean().reset_index().groupby(['YearGroup']).sum().reset_index()['PosCountNorm'],
            name='Line 2')
        fig.update_layout(yaxis_range=[0,50])

        return fig

# main bar chart
@app.callback(
    Output('pos_groups_dropdown_bar1_sub', 'value'),
    Output('pos_groups_dropdown_bar1_sub', 'options'),
    [Input('pos_groups_dropdown_bar1_main', 'value')])
def bar_tag_options(mains):

    values = []
    options = []
    for main in mains:
        value = list(data_parser.pos_categories[main].keys())
        values.extend(value)
        options.extend(data_parser.list_to_dash_option_dict(value))
    
    return values, options


@app.callback(
    Output('bar_chart', 'figure'), 
    Input('update_bar_button', 'n_clicks'), # Only pressing the button initiates the function
    [State('pos_groups_dropdown_bar1_main', 'value')],
    [State('pos_groups_dropdown_bar1_sub', 'value')],
    [State('year-group-number-bar', 'value')])

def display_bar_chart(n_clicks, values0, values1, periods):

    if n_clicks is not None:
        bins = pd.interval_range(start=1680, end=1800, periods=periods, closed='right')
        labels = list(bins.astype(str))

        df = data_parser.df
        df = df.groupby(['ID', 'SenderSex', 'SenderRank', 'RelCode', 'Tags', 'Year', 'WordCount']).size().to_frame(name = 'PosCount').reset_index()
        df['PosCountNorm'] = df['PosCount']/df['WordCount']*100
        
        df['Year'] = df['Year'].astype('int')
        df['YearGroup'] = pd.cut(df['Year'], bins=bins,include_lowest=True, labels=labels, precision=0)
        df['YearGroup'] = df['YearGroup'].astype("str")
        df = df.groupby(['YearGroup', 'Tags', 'SenderSex']).mean().reset_index()

        fig = go.Figure()
        mask = df['Tags'].isin(values1)
        fig= px.bar(
            data_frame=df[mask].groupby(['Tags', 'YearGroup', 'SenderSex']).mean().reset_index(),
            x='YearGroup', 
            y='PosCountNorm',
            range_y=[0,30],
            labels={
                'YearGroup': 'Year', 
                'PosCountNorm':'Percentage'},
            hover_data=['Tags'],
            color='SenderSex',
            barmode='group',
            title='Main Bar Chart')
        fig.update_layout(yaxis_range=[0,50])

        return fig

# TEsting wordcount bar chart
@app.callback(
    Output('count_bar_chart', 'figure'), 
    Input('update_count_button', 'n_clicks'), # Only pressing the button initiates the function
    [State('pos_groups_dropdown_count_main', 'value')],
    [State('pos_groups_dropdown_count_sub', 'value')],
    [State('year-group-number-count', 'value')])

def display_bar_chart(n_clicks, values0, values1, periods):

    if n_clicks is not None:
        bins = pd.interval_range(start=1680, end=1800, periods=periods, closed='right')
        labels = list(bins.astype(str))

        df = data_parser.df
        df = df.groupby(['ID', 'SenderSex', 'SenderRank', 'RelCode', 'Tags', 'Year', 'WordCount']).size().to_frame(name = 'PosCount').reset_index()
        df['PosCountNorm'] = df['PosCount']/df['WordCount']*100
        
        df['Year'] = df['Year'].astype('int')
        df['YearGroup'] = pd.cut(df['Year'], bins=bins,include_lowest=True, labels=labels, precision=0)
        df['YearGroup'] = df['YearGroup'].astype("str")
        df = df.groupby(['YearGroup', 'Tags', 'SenderSex']).mean().reset_index()

        fig = go.Figure()
        mask = df['Tags'].isin(values1)
        fig= px.bar(
            data_frame=df[mask].groupby(['Tags', 'YearGroup', 'SenderSex']).mean().reset_index(),
            x='YearGroup', 
            y='PosCount',
            range_y=[0,200],
            labels={
                'YearGroup': 'Year', 
                'PosCount':'Number of words'},
            hover_data=['Tags'],
            color='SenderSex',
            barmode='group',
            title='Wordcount of each period')
        fig.update_layout(yaxis_range=[0,200])

        return fig

# Dynamic grouping bar chart
@app.callback(
    Output('dynamic-subattribute-selection', 'value'),
    Output('dynamic-subattribute-selection', 'options'),
    Input('dynamic-attribute-selection', 'value'))
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
