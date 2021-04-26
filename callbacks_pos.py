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
from multiprocessing import  Pool
import time

from app import app
import globals

data_parser = globals.data_parser

df = data_parser.df


def parallelize_dataframe(df, func, n_cores=4):
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df


def initial_poscount_groupby(df):
    return df.groupby(['YearGroup', 'ID', 'Sender', 'SenderSex', 'SenderRank', 'RelCode', 'Tags', 'WordCount']).size().to_frame(name = 'PosCount').reset_index()

def wordcount_groupby(df):
    return df.groupby(['ID','YearGroup']).min().reset_index().groupby(['YearGroup']).sum().reset_index()['WordCount']

def poscount_groupby(df):
    return df.groupby(['YearGroup']).sum().reset_index()['PosCount']

# Callback for the slider element
@app.callback(
    Output('line_slider_output', 'children'), # Modified string with the years is passed to the Div-element
    Output('line_slider_values', 'value'), # Unmodified list of the selected years is passed to the next callback 
    Input('line_time_slider', 'value'))
def set_years(selected_years):
    years = 'Selected period: {start} - {end}'.format(start=selected_years[0], end=selected_years[1])

    return years, selected_years


for i in range (0,11):
    @app.callback(
        Output(f'pos_groups_dropdown_{i}_sub', 'value'),
        Output(f'pos_groups_dropdown_{i}_sub', 'options'),
        [Input(f'pos_groups_dropdown_{i}_main', 'value')],
        State('user-browser-store', 'data'))
    def line_group_pos_options(mains, data):

        values = []
        options = []
        for main in mains:
            value = data_parser.get_pos_categories(data)[main]
            values.extend(value)
            options.extend(data_parser.pos_options_with_hover(data, main))
        
        return values, options


for i in range (0,11):
    @app.callback(
        Output(f'line_senderrank_sub_{i}', 'value'),
        Output(f'line_senderrank_sub_{i}', 'options'),
        Input(f'line_senderrank_main_{i}', 'value'),
        State('user-browser-store', 'data'))
    def line_group_rank_options(main, data):

        values = []
        options = []
        value = data_parser.rank_categories[main]
        values.extend(value)
        options.extend(data_parser.dict_to_dash_options_with_hover(data_parser.rank_categories[main]))
        
        return values, options

for i in range (0,11):
    @app.callback(
        Output(f'line_relationship_sub_{i}', 'value'),
        Output(f'line_relationship_sub_{i}', 'options'),
        Input(f'line_relationship_main_{i}', 'value'),
        State('user-browser-store', 'data'))
    def line_group_rel_options(main, data):

        values = []
        options = []
        value = data_parser.relationship_categories[main]
        values.extend(value)
        options.extend(data_parser.dict_to_dash_options_with_hover(data_parser.relationship_categories[main]))
        
        return values, options

for i in range(1,11):
    @app.callback(
        Output(f'line_store_{i}', 'data'),
        Input('update_line_button', 'n_clicks'), # Only pressing the button initiates the function
        Input('update_line_button_1', 'n_clicks'), # Only pressing the button initiates the function
        Input('dummy_div', 'children'),
        Input(f'line_name_{i}', 'value'),
        [Input(f'pos_groups_dropdown_{i}_sub', 'value')],
        [Input(f'line_sex_{i}', 'value')],
        Input(f'line_senderrank_main_{i}', 'value'),
        [Input(f'line_senderrank_sub_{i}', 'value')],
        Input(f'line_relationship_main_{i}', 'value'),
        [Input(f'line_relationship_sub_{i}', 'value')])
    def save_selection(clicks1, clicks2, aux, name, pos_sub, sex, rank_main, rank_sub, rel_main, rel_sub):
        return {
            'name': name,
            'pos_sub': pos_sub,
            'sex': sex,
            'rank_main': rank_main,
            'rank_sub': rank_sub,
            'rel_main': rel_main,
            'rel_sub': rel_sub
        }


@app.callback(
    Output('line_graph', 'figure'), 
    Output('bar_df', 'children'),
    Output('bar_names', 'children'),
    Input('update_line_button', 'n_clicks'), # Only pressing the button initiates the function
    Input('update_line_button_1', 'n_clicks'), # Only pressing the button initiates the function
    State('line_graph_name', 'value'),
    [State('inherit_pos', 'value')],
    [State('inherit_attributes', 'value')],
    [State('pos_groups_dropdown_0_sub', 'value')],
    [State('line_sex_0', 'value')],
    State('line_senderrank_main_0', 'value'),
    [State('line_senderrank_sub_0', 'value')],
    State('line_relationship_main_0', 'value'),
    [State('line_relationship_sub_0', 'value')],
    [State(f'line_store_{i}', 'data') for i in range(1,11)],
    [State('line_period_length', 'value')],
    [State('line_time_slider', 'value')],
    [State('line_visibility', 'value')],
    State('user-browser-store', 'data'))
def display_line_graph(
    n_clicks, n_clicks_1, graph_name, inherit_pos, inherit_attributes, 
    pos_sub_0, sex_0, rank_main_0, rank_sub_0, rel_main_0, rel_sub_0, 
    line1, line2, line3, line4, line5, line6, line7, line8, line9, line10, 
    periods, years, visibility, data):

    if n_clicks == 0 and n_clicks_1 == 0:
        line1 = {
            'name': 'Line 1',
            'pos_sub': pos_sub_0,
            'sex': sex_0,
            'rank_main': rank_main_0,
            'rank_sub': rank_sub_0,
            'rel_main': rel_main_0,
            'rel_sub': rel_sub_0
        }

    start = years[0]
    end = years[1]
    full_period = end - start
    modulo = full_period % periods

    if modulo == 0:
        end_a = end - periods
        end_b = end_a + periods + 1
    else:
        end_a = end - modulo
        end_b = end_a + modulo + 1

    starts = np.arange(start, end_a, periods).tolist()
    tuples = [(start, start+periods) for start in starts]
    tuples.append(tuple([end_a, end_b]))

    bins = pd.IntervalIndex.from_tuples(tuples, closed='left')
    
    original_labels = list(bins.astype(str))
    new_labels = ['{} - {}'.format(b.strip('[)').split(', ')[0], int(b.strip('[)').split(', ')[1])-1) for b in list(bins.astype(str))]
    label_dict = dict(zip(original_labels, new_labels))

    df = data_parser.df.copy()
    
    # Assign each row to a period
    df['Year'] = df['Year'].astype('int')
    df['YearGroup'] = pd.cut(df['Year'], bins=bins,include_lowest=True, labels=new_labels, precision=0)
    df['YearGroup'] = df['YearGroup'].astype("str")
    df = df.replace(label_dict)

    # Group the data to get count of each POS tag in the data
    # df = poscount_groupby(df)
    df = parallelize_dataframe(df, initial_poscount_groupby)

    fig = go.Figure()
    lines_df = pd.DataFrame()

    line_dict = {
        1: line1,
        2: line2,
        3: line3,
        4: line4,
        5: line5,
        6: line6,
        7: line7,
        8: line8,
        9: line9,
        10: line10
    }

    # Visibility list is sorted to have them in the natural order user is expecting regardless of the choosing order
    visibility.sort()
    for line in visibility:
        
        if '1' in inherit_pos:
            pos_sub = pos_sub_0
        else:
            pos_sub = line_dict[line]['pos_sub']
        if '1' in inherit_attributes:
            sex = sex_0
            rank_main = rank_main_0
            rank_sub = rank_sub_0
            rel_main = rel_main_0
            rel_sub = rel_sub_0
        else:
            sex = line_dict[line]['sex']
            rank_main = line_dict[line]['rank_main']
            rank_sub = line_dict[line]['rank_sub']
            rel_main = line_dict[line]['rel_main']
            rel_sub = line_dict[line]['rel_sub']

        helper_dict = {
            'Tags': pos_sub,
            'SenderSex': sex,
            'SenderRank': list(flatten([data_parser.rank_categories[rank_main][sub] for sub in rank_sub])),
            'RelCode': list(flatten([data_parser.relationship_categories[rel_main][sub] for sub in rel_sub]))
        }
        # mask 1
        mask = df[['Tags', 'SenderSex', 'SenderRank', 'RelCode']].isin(helper_dict).all(axis=1)
        temp = df[mask].copy()
        
        # Grouping by desired attributes may lead to loss of some periods
        # Here we add mock data for those periods so the graph is shown correctly
        for p in new_labels:
            if p not in list(temp['YearGroup'].unique()):
                temp = temp.append(
                    {
                        'YearGroup': p,
                        'ID': 'Not found',
                        'Sender': 'Not found',
                        'SenderSex': 'Not found',
                        'SenderRank': 'Not found',
                        'RelCode': 'Not found',
                        'Tags': 'Not found',
                        'WordCount': 0,
                        'PosCount': 0
                    }, ignore_index=True
                )

        word_counts = parallelize_dataframe(temp, wordcount_groupby)
        pos_counts = parallelize_dataframe(temp, poscount_groupby)

        fig.add_scatter(
            x=new_labels, 
            y=(pos_counts/word_counts).fillna(0)*100,
            name=line_dict[line]['name'],
            showlegend=True,
            connectgaps=True)
        # Append to DF for bar chart
        temp['Line'] = [line_dict[line]['name']] * len(temp.index)
        lines_df = lines_df.append(temp)

    fig.update_layout(
        title=graph_name,
        xaxis_title="Period",
        yaxis_title="%"
    )

    # Figure shows as autoscaled from the beginning, as values are not set
    # tozero mode forces y axis to start from zero to avoid misleading visualizations
    fig.update_yaxes(rangemode='tozero')

    # Different lines having same POS messes up the dataframe index 
    # which then messes up json converting, creating new index solves this
    lines_df.reset_index(drop=True, inplace=True)
    
    # Makes a list of the line names in right order to be sent to the bar graph
    line_names = [[value["name"] for key, value in line_dict.items() if value is not None][i] for i in np.array(visibility)-1]

    return fig, lines_df.to_json(), line_names

    #return go.Figure(), pd.DataFrame(columns=['YearGroup', 'ID', 'Sender', 'SenderSex', 'SenderRank', 'RelCode', 'WordCount', 'Line']).to_json()


def line_groupby_id(df):
    return df.groupby(['ID', 'Line']).min().reset_index()

def line_groupby_sender(df):    
    return df.groupby(['Sender', 'Line']).min().reset_index()

# Testing wordcount bar chart
@app.callback(
    Output('count_bar_chart', 'figure'), 
    Output('size_info', 'children'),
    [Input('bar_df', 'children')],
    Input('bar_names', 'children'),
    Input('bar_what_count', 'value'),
    Input('bar_groub_by', 'value'))
def display_wordcount_chart(json, line_names, what_count, group_by_what):

        lines_df = pd.read_json(json)
        
        grouped = lines_df.groupby('ID').min()
        words = grouped['WordCount'].sum()
        letters = len(lines_df['ID'].unique())
        people = len(lines_df['Sender'].unique())
        
        final_groupby = [group_by_what, 'YearGroup', 'Line']

        lines_df['PeopleCount'] = [1] * len(lines_df['WordCount'])
        lines_df['LetterCount'] = [1] * len(lines_df['WordCount'])

        if what_count == 'words':
            y = 'WordCount'
            lines_df = parallelize_dataframe(lines_df, line_groupby_id)
        elif what_count == 'letters':
            y = 'LetterCount'
            lines_df = parallelize_dataframe(lines_df, line_groupby_id)
        elif what_count == 'people':
            y = 'PeopleCount'
            lines_df = parallelize_dataframe(lines_df, line_groupby_sender)
        
        lines_df = lines_df.groupby(final_groupby).sum().reset_index()

        selection_info = f"Number of non-unique words: {words}, number of letters: {letters}, number of senders: {people}"

        fig = px.bar(
            data_frame=lines_df,
            x='YearGroup', 
            y=y,
            labels={
                'YearGroup': 'Period', 
                y:'Number of {}'.format(what_count)},
            hover_data=[group_by_what],
            color='Line',
            barmode='group',
            category_orders={'Period':line_names, 'Line': line_names},
            title='Number of {} for each line, grouped by {}'.format(what_count, group_by_what))
        
        fig.update_xaxes(categoryorder='category ascending')

        fig.update_layout()

        return fig, selection_info
