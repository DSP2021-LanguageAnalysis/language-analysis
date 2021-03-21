from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import io

from app import app
from pos_tab import PosTab
#from data_parser import DataParser
from df_parser import DataParser

pos_tab = PosTab()
data_parser = DataParser()
# df = data_parser.letters_to_df()
# pos_counts = data_parser.get_pos_counts()
# nn1_MF = data_parser.get_mfn_ratio()
# tag_MF = data_parser.get_mfn_tag()

@app.callback(Output('pos_graph', 'figure'), 
            [Input('pos_dropdown', 'value')],
            State('memory', 'data'))
def display_pos_graphs(selected_values, data):

    if selected_values is None:
        raise PreventUpdate
    else:
        df = pd.read_csv(io.StringIO(data))
        pos_counts = data_parser.get_pos_counts(df)
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
    Input('pos_groups_dropdown_2', 'value')],
    State('memory', 'data'))
def display_grouped_pos_graphs(values1, values2, data):

    if values1 is None and values2 is None:
        raise PreventUpdate
    else:
        fig = go.Figure()
        df = pd.read_csv(io.StringIO(data))
        pos_counts = data_parser.get_pos_counts(df)
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
    [Input('year-group-number', 'value')],
    State('memory', 'data'))
def display_grouped_pos_graphs(value, data):

    if value is None:
        raise PreventUpdate
    else:
        bins = pd.interval_range(start=1700, end=1800, periods=value, closed='right')
        labels = list(bins.astype(str))
        #df = nn1_MF.copy()
        df = pd.read_csv(io.StringIO(data))
        df = data_parser.get_mfn_ratio(df)
        df['Year'] = df['Year'].astype('int')
        df['YearGroup'] = pd.cut(df['Year'], bins=bins,include_lowest=True, labels=labels, precision=0)
        df['YearGroup'] = df['YearGroup'].astype("str")
        df = df.groupby(['YearGroup', 'SenderSex']).mean().reset_index()

        return px.bar(df, x="YearGroup", y="PosCountNorm", color='SenderSex', barmode='group', title='Dynamically group years')  

@app.callback(
    Output('M/F_barChart', 'figure'), 
    [Input('F/M_dropdown_1', 'value')],
    State('memory', 'data'))
def display_multiple_tags_barchart(values, data):

    if values is None:
        raise PreventUpdate
    else:
        df = pd.read_csv(io.StringIO(data))
        tag_MF = data_parser.get_mfn_tag(df)
        mask = tag_MF['Tags'].isin(values)
        fig= px.bar(
            # can choose only one tag at a time
            data_frame=tag_MF[mask].groupby(['Year', 'SenderSex', 'Tags']).mean().reset_index(),
            x='Year', 
            y='PosCountNorm',
            range_y=[0,30],
            labels={
                'Year': 'Year', 
                'PosCountNorm':'Percentage'},
            hover_data=['Tags'],
            color='SenderSex',
            barmode='group',
            title='Compare male and female tags')

        return fig

@app.callback(
    Output('dynamic-subattribute-selection', 'value'),
    Output('dynamic-subattribute-selection', 'options'),
    Input('dynamic-attribute-selection', 'value'),
    State('memory', 'data'))
def pos_selection(attribute_selection, data):
    if attribute_selection is None:
        raise PreventUpdate
    else:
        df = pd.read_csv(io.StringIO(data))
        value, options = pos_tab.selection(df, attribute_selection)
        return value, options

@app.callback(
    Output('dynamic-attribute-bar', 'figure'), 
    Input('pos_button', 'n_clicks'), # Only pressing the button initiates the function
    State('dynamic-attribute-selection', 'value'),
    State('dynamic-subattribute-selection', 'value'),
    State('pos-year-group-number', 'value'),
    State('memory', 'data'))
def pos_dynamic_attributes(clicks, input1, input2, period_count, data):
    df = pd.read_csv(io.StringIO(data))
    pos_counts = data_parser.get_pos_counts(df)
    fig = pos_tab.dynamic_attributes(df, pos_counts, input1, input2, period_count)
    return fig
