import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from pandas.core.common import flatten
import math
import numpy as np

from app import app
import globals

data_parser = globals.data_parser

df = data_parser.df
pos_counts = data_parser.get_pos_counts()
nn1_MF = data_parser.get_mfn_ratio()
tag_MF = data_parser.get_mfn_tag()


# Callback for the slider element
@app.callback(
    Output('line_slider_output', 'children'), # Modified string with the years is passed to the Div-element
    Output('line_slider_values', 'value'), # Unmodified list of the selected years is passed to the next callback 
    Input('line_time_slider', 'value'))
def set_years(selected_years):
    years = 'Selected period: {start} - {end}'.format(start=selected_years[0], end=selected_years[1])

    return years, selected_years


for i in range (0,4):
    @app.callback(
        Output(f'pos_groups_dropdown_{i}_sub', 'value'),
        Output(f'pos_groups_dropdown_{i}_sub', 'options'),
        [Input(f'pos_groups_dropdown_{i}_main', 'value')],
        State('session', 'data'))
    def line_group_pos_options(mains, data):

        values = []
        options = []
        for main in mains:
            value = data_parser.get_pos_categories(data)[main]
            values.extend(value)
            options.extend(data_parser.pos_options_with_hover(data, main))
        
        return values, options


for i in range (1,4):
    @app.callback(
        Output(f'line_senderrank_sub_{i}', 'value'),
        Output(f'line_senderrank_sub_{i}', 'options'),
        Input(f'line_senderrank_main_{i}', 'value'),
        State('session', 'data'))
    def line_group_rank_options(main, data):

        values = []
        options = []
        value = data_parser.rank_categories[main]
        values.extend(value)
        options.extend(data_parser.dict_to_dash_options_with_hover(data_parser.rank_categories[main]))
        
        return values, options

for i in range (1,4):
    @app.callback(
        Output(f'line_relationship_sub_{i}', 'value'),
        Output(f'line_relationship_sub_{i}', 'options'),
        Input(f'line_relationship_main_{i}', 'value'),
        State('session', 'data'))
    def line_group_rel_options(main, data):

        values = []
        options = []
        value = data_parser.relationship_categories[main]
        values.extend(value)
        options.extend(data_parser.dict_to_dash_options_with_hover(data_parser.relationship_categories[main]))
        
        return values, options


@app.callback(
    Output('line_graph', 'figure'), 
    Input('update_line_button', 'n_clicks'), # Only pressing the button initiates the function
    Input('update_line_button_1', 'n_clicks'), # Only pressing the button initiates the function
    State('line_graph_name', 'value'),
    [State('inherit_pos', 'value')],
    State('line_name_1', 'value'),
    State('line_name_2', 'value'),
    State('line_name_3', 'value'),
    [State('pos_groups_dropdown_0_main', 'value')],
    [State('pos_groups_dropdown_1_main', 'value')],
    [State('pos_groups_dropdown_2_main', 'value')],
    [State('pos_groups_dropdown_3_main', 'value')],
    [State('pos_groups_dropdown_0_sub', 'value')],
    [State('pos_groups_dropdown_1_sub', 'value')],
    [State('pos_groups_dropdown_2_sub', 'value')],
    [State('pos_groups_dropdown_3_sub', 'value')],
    [State('line_sex_1', 'value')],
    [State('line_sex_2', 'value')],
    [State('line_sex_3', 'value')],
    State('line_senderrank_main_1', 'value'),
    [State('line_senderrank_sub_1', 'value')],
    State('line_senderrank_main_2', 'value'),
    [State('line_senderrank_sub_2', 'value')],
    State('line_senderrank_main_3', 'value'),
    [State('line_senderrank_sub_3', 'value')],
    State('line_relationship_main_1', 'value'),
    [State('line_relationship_sub_1', 'value')],
    State('line_relationship_main_2', 'value'),
    [State('line_relationship_sub_2', 'value')],
    State('line_relationship_main_3', 'value'),
    [State('line_relationship_sub_3', 'value')],
    [State('line_period_length', 'value')],
    [State('line_time_slider', 'value')],
    [State('line_visibility', 'value')],
    State('session', 'data'))
def display_line_graph(n_clicks, n_clicks_1, graph_name, inherit_pos, name_1, name_2, name_3, pos_main_0, pos_main_1, pos_main_2, pos_main_3, pos_sub_0, pos_sub_1, pos_sub_2, pos_sub_3, sex_1, sex_2, sex_3, rank_main_1, rank_sub_1, rank_main_2, rank_sub_2, rank_main_3, rank_sub_3, rel_main_1, rel_sub_1, rel_main_2, rel_sub_2, rel_main_3, rel_sub_3, periods, years, visibility, data):

    if n_clicks >= 0 or n_clicks_1 >= 0:


        if '1' in inherit_pos:
            pos_sub_0 = data_parser.include_ditto_tags_to_pos_list(pos_sub_0)
            pos_sub_1, pos_sub_2, pos_sub_3 = pos_sub_0, pos_sub_0, pos_sub_0
        else:
            pos_sub_1 = data_parser.include_ditto_tags_to_pos_list(pos_sub_1)
            pos_sub_2 = data_parser.include_ditto_tags_to_pos_list(pos_sub_2)
            pos_sub_3 = data_parser.include_ditto_tags_to_pos_list(pos_sub_3)

        start = years[0]
        end = years[1]
        full_period = end - start
        modulo = full_period % periods
        number_of_periods = math.floor(full_period / periods)

        if modulo == 0:
            bins = pd.interval_range(start=start, end=end, periods=number_of_periods, closed='left')
        else:
            end = end - modulo
            starts = np.arange(start, end, periods).tolist()

            tuples = [(start, start+periods) for start in starts]
            tuples.append(tuple([end, end+modulo]))

            bins = pd.IntervalIndex.from_tuples(tuples, closed='left')
        
        original_labels = list(bins.astype(str))
        new_labels = ['{} - {}'.format(b.strip('[)').split(', ')[0], int(b.strip('[)').split(', ')[1])-1) for b in list(bins.astype(str))]
        label_dict = dict(zip(original_labels, new_labels))

        df = data_parser.df
        df = df.groupby(['ID', 'SenderSex', 'SenderRank', 'RelCode', 'Tags', 'Year', 'WordCount']).size().to_frame(name = 'PosCount').reset_index()
        df['PosCountNorm'] = df['PosCount']/df['WordCount']*100
        
        df['Year'] = df['Year'].astype('int')
        df['YearGroup'] = pd.cut(df['Year'], bins=bins,include_lowest=True, labels=new_labels, precision=0)
        df['YearGroup'] = df['YearGroup'].astype("str")
        #df = df.groupby(['YearGroup', 'Tags', 'SenderSex', 'SenderRank', 'RelCode']).mean().reset_index()
        df = df.replace(label_dict)

        # x = df['YearGroup'].dropna().unique()
        # x.sort(axis=0)
        # print(x)
        # print(new_labels)

        fig = go.Figure()
        if '1' in visibility:
            helper_dict = {
                'Tags': pos_sub_1,
                'SenderSex': sex_1,
                'SenderRank': list(flatten([data_parser.rank_categories[rank_main_1][rank_sub] for rank_sub in rank_sub_1])),
                'RelCode': list(flatten([data_parser.relationship_categories[rel_main_1][rel_sub] for rel_sub in rel_sub_1]))
            }
            mask = df[['Tags', 'SenderSex', 'SenderRank', 'RelCode']].isin(helper_dict).all(axis=1)
            fig.add_scatter(
                x=new_labels, 
                y=df[mask].groupby(['Tags', 'YearGroup']).mean().reset_index().groupby(['YearGroup']).sum().reset_index()['PosCountNorm'],
                name=name_1)
        if '2' in visibility:
            helper_dict = {
                'Tags': pos_sub_2,
                'SenderSex': sex_2,
                'SenderRank': list(flatten([data_parser.rank_categories[rank_main_2][rank_sub] for rank_sub in rank_sub_2])),
                'RelCode': list(flatten([data_parser.relationship_categories[rel_main_2][rel_sub] for rel_sub in rel_sub_2]))
            }
            mask = df[['Tags', 'SenderSex', 'SenderRank', 'RelCode']].isin(helper_dict).all(axis=1)
            fig.add_scatter(
                x=new_labels, 
                y=df[mask].groupby(['Tags', 'YearGroup']).mean().reset_index().groupby(['YearGroup']).sum().reset_index()['PosCountNorm'],
                name=name_2)
        if '3' in visibility:
            helper_dict = {
                'Tags': pos_sub_3,
                'SenderSex': sex_3,
                'SenderRank': list(flatten([data_parser.rank_categories[rank_main_3][rank_sub] for rank_sub in rank_sub_3])),
                'RelCode': list(flatten([data_parser.relationship_categories[rel_main_3][rel_sub] for rel_sub in rel_sub_3]))
            }
            mask = df[['Tags', 'SenderSex', 'SenderRank', 'RelCode']].isin(helper_dict).all(axis=1)
            fig.add_scatter(
                x=new_labels, 
                y=df[mask].groupby(['Tags', 'YearGroup']).mean().reset_index().groupby(['YearGroup']).sum().reset_index()['PosCountNorm'],
                name=name_3)

        fig.update_layout(
            title=graph_name,
            yaxis_range=[0,50],
            xaxis_title="Period",
            yaxis_title="%"
        )

        return fig

@app.callback(
    Output('pos_groups_dropdown_1_main', 'options'),
    Output('pos_groups_dropdown_2_main', 'options'),
    Output('pos_groups_dropdown_3_main', 'options'),
    #Input('update_customs_button', 'n_clicks'),
    Input('session', 'data'))
def update_options(data):

    options = data_parser.list_to_dash_option_dict(list(data_parser.get_pos_categories(data).keys()))
    return options, options, options


# main bar chart
@app.callback(
    Output('pos_groups_dropdown_bar1_sub', 'value'),
    Output('pos_groups_dropdown_bar1_sub', 'options'),
    [Input('pos_groups_dropdown_bar1_main', 'value')],
    State('session', 'data'))
def bar_tag_options(mains, data):

    values = []
    options = []
    for main in mains:
        value = data_parser.get_pos_categories(data)[main]
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
    Input('update_line_button', 'n_clicks'), # Only pressing the button initiates the function
    Input('update_line_button_1', 'n_clicks'), # Only pressing the button initiates the function
    Input('bar_what_count', 'value'),
    Input('bar_groub_by', 'value'),
    State('line_graph_name', 'value'),
    [State('inherit_pos', 'value')],
    State('line_name_1', 'value'),
    State('line_name_2', 'value'),
    State('line_name_3', 'value'),
    [State('pos_groups_dropdown_0_sub', 'value')],
    [State('pos_groups_dropdown_1_sub', 'value')],
    [State('pos_groups_dropdown_2_sub', 'value')],
    [State('pos_groups_dropdown_3_sub', 'value')],
    [State('line_sex_1', 'value')],
    [State('line_sex_2', 'value')],
    [State('line_sex_3', 'value')],
    State('line_senderrank_main_1', 'value'),
    [State('line_senderrank_sub_1', 'value')],
    State('line_senderrank_main_2', 'value'),
    [State('line_senderrank_sub_2', 'value')],
    State('line_senderrank_main_3', 'value'),
    [State('line_senderrank_sub_3', 'value')],
    State('line_relationship_main_1', 'value'),
    [State('line_relationship_sub_1', 'value')],
    State('line_relationship_main_2', 'value'),
    [State('line_relationship_sub_2', 'value')],
    State('line_relationship_main_3', 'value'),
    [State('line_relationship_sub_3', 'value')],
    [State('line_period_length', 'value')],
    [State('line_time_slider', 'value')],
    [State('line_visibility', 'value')])
def display_wordcount_chart(n_c1, n_c2, what_count, group_by_what, graph_name, inherit_pos, name_1, name_2, name_3, pos_sub_0, pos_sub_1, pos_sub_2, pos_sub_3, sex_1, sex_2, sex_3, rank_main_1, rank_sub_1, rank_main_2, rank_sub_2, rank_main_3, rank_sub_3, rel_main_1, rel_sub_1, rel_main_2, rel_sub_2, rel_main_3, rel_sub_3, periods, years, visibility):

 
        start = years[0]
        end = years[1]
        full_period = end - start
        modulo = full_period % periods
        number_of_periods = math.floor(full_period / periods)

        if modulo == 0:
            bins = pd.interval_range(start=start, end=end, periods=number_of_periods, closed='left')
        else:
            end = end - modulo
            starts = np.arange(start, end, periods).tolist()

            tuples = [(start, start+periods) for start in starts]
            tuples.append(tuple([end, end+modulo]))

            bins = pd.IntervalIndex.from_tuples(tuples, closed='left')
        
        original_labels = list(bins.astype(str))
        new_labels = ['{} - {}'.format(b.strip('[)').split(', ')[0], int(b.strip('[)').split(', ')[1])-1) for b in list(bins.astype(str))]
        label_dict = dict(zip(original_labels, new_labels))

        df = data_parser.df
        df['Year'] = df['Year'].astype('int')
        df['YearGroup'] = pd.cut(df['Year'], bins=bins,include_lowest=True, labels=new_labels, precision=0)
        df['YearGroup'] = df['YearGroup'].astype("str")
        df = df.replace(label_dict)

        initial_groupby = ['YearGroup', 'ID', 'Sender', 'Tags', 'SenderSex', 'SenderRank', 'RelCode']
        final_groupby = [group_by_what, 'YearGroup', 'Line']

        df = df.groupby(initial_groupby).size().to_frame(name = 'Count').reset_index()

        fig = go.Figure()

        lines_df = pd.DataFrame()

        if '1' in visibility:
            helper_dict = {
                'Tags': pos_sub_1,
                'SenderSex': sex_1,
                'SenderRank': list(flatten([data_parser.rank_categories[rank_main_1][rank_sub] for rank_sub in rank_sub_1])),
                'RelCode': list(flatten([data_parser.relationship_categories[rel_main_1][rel_sub] for rel_sub in rel_sub_1]))
            }
            mask = df[['Tags', 'SenderSex', 'SenderRank', 'RelCode']].isin(helper_dict).all(axis=1)
            temp = df[mask].copy()
            temp['Line'] = [name_1] * len(temp.index)
            lines_df = lines_df.append(temp)

        if '2' in visibility:
            helper_dict = {
                'Tags': pos_sub_2,
                'SenderSex': sex_2,
                'SenderRank': list(flatten([data_parser.rank_categories[rank_main_2][rank_sub] for rank_sub in rank_sub_2])),
                'RelCode': list(flatten([data_parser.relationship_categories[rel_main_2][rel_sub] for rel_sub in rel_sub_2]))
            }
            mask = df[['Tags', 'SenderSex', 'SenderRank', 'RelCode']].isin(helper_dict).all(axis=1)
            temp = df[mask].copy()
            temp['Line'] = [name_2] * len(temp.index)
            lines_df = lines_df.append(temp)

        if '3' in visibility:
            helper_dict = {
                'Tags': pos_sub_3,
                'SenderSex': sex_3,
                'SenderRank': list(flatten([data_parser.rank_categories[rank_main_3][rank_sub] for rank_sub in rank_sub_3])),
                'RelCode': list(flatten([data_parser.relationship_categories[rel_main_3][rel_sub] for rel_sub in rel_sub_3]))
            }
            mask = df[['Tags', 'SenderSex', 'SenderRank', 'RelCode']].isin(helper_dict).all(axis=1)
            temp = df[mask].copy()
            temp['Line'] = [name_3] * len(temp.index)
            lines_df = lines_df.append(temp)

        fig = px.bar(
            data_frame=lines_df.groupby(final_groupby).sum().reset_index(),
            x='YearGroup', 
            y='Count',
            labels={
                'YearGroup': 'Period', 
                'Count':'Number of {}'.format(what_count)},
            hover_data=[group_by_what],
            color='Line',
            barmode='group',
            title='Number of {} for each line, grouped by {}'.format(what_count, group_by_what))

        fig.update_layout()

        return fig
