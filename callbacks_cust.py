import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate

from app import app
import globals

data_parser = globals.data_parser


@app.callback(
    Output('user-pos-store', 'data'),
    Input('add_pos_group_button', 'n_clicks'),
    [State('pos_group_name', 'value')],
    [State('pos_group_tags', 'value')],
    State('user-pos-store', 'data'))
def add_pos_group(n_clicks, name, tags, data):
    
    if n_clicks > 0:
        if data is None:
            data = dict()
        tags = tags.split(';')
        data[name] = tags
    
    return data


@app.callback(
    Output('cust_pos_groups', 'children'),
    Input('user-pos-store', 'data'))
def view_pos_groups(data):

    if data is not None:
        children = []
        for (n, t) in data.items():
            children.append(html.P('{}: {}'.format(n, ', '.join(list(t)))))
        
        return children


for i in range (0,11):
    @app.callback(
        Output(f'pos_groups_dropdown_{i}_main', 'options'),
        Input('user-pos-store', 'data'))
    def include_pos_groups_line(data):

        if data is not None:
            return data_parser.list_to_dash_option_dict(list(data_parser.get_pos_categories(data).keys()))
        return data_parser.list_to_dash_option_dict(list(data_parser.pos_categories.keys()))


@app.callback(
    Output('pos_tm_main', 'options'),
    Input('user-pos-store', 'data'))
def include_pos_groups_topicmodel(data):

    if data is not None:
        return data_parser.list_to_dash_option_dict(list(data_parser.get_pos_categories(data).keys()))
    return data_parser.list_to_dash_option_dict(list(data_parser.pos_categories.keys()))



@app.callback(
    Output('user-relationship-store', 'data'),
    Input('add_relationship_group_button', 'n_clicks'),
    [State('relationship_group_name', 'value')],
    [State('relationship_group_tags', 'value')],
    State('user-relationship-store', 'data'))
def add_relationship_group(n_clicks, name, tags, data):
    
    if n_clicks > 0:
        if data is None:
            data = dict()
            data['Custom'] = {}
        tags = tags.split(';')
        data['Custom'][name] = tags
    
    return data


@app.callback(
    Output('cust_relationship_groups', 'children'),
    Input('user-relationship-store', 'data'))
def view_rel_groups(data):

    if data is not None:

        children = []
        for (n, t) in data['Custom'].items():
            children.append(html.P('{}: {}'.format(n, ', '.join(list(t)))))
        
        return children

for i in range (0,11):
    @app.callback(
        Output(f'line_relationship_main_{i}', 'options'),
        Input('user-relationship-store', 'data'))
    def include_rel_groups_line(data):

        if data is not None:
            return data_parser.list_to_dash_option_dict(list(data_parser.get_rel_categories(data).keys()))
        return data_parser.list_to_dash_option_dict(list(data_parser.relationship_categories.keys()))
    
@app.callback(
    Output('relationship-main', 'options'),
    Input('user-relationship-store', 'data'))
def include_rel_groups_topicmodel(data):

    if data is not None:
        return data_parser.list_to_dash_option_dict(list(data_parser.get_rel_categories(data).keys()))
    return data_parser.list_to_dash_option_dict(list(data_parser.relationship_categories.keys()))


@app.callback(
    Output('user-rank-store', 'data'),
    Input('add_rank_group_button', 'n_clicks'),
    [State('rank_group_name', 'value')],
    [State('rank_group_tags', 'value')],
    State('user-rank-store', 'data'))
def add_rank_group(n_clicks, name, tags, data):
    
    if n_clicks > 0:
        if data is None:
            data = dict()
            data['Custom'] = {}
        tags = tags.split(';')
        data['Custom'][name] = tags
    
    return data

@app.callback(
    Output('cust_rank_groups', 'children'),
    Input('user-rank-store', 'data'))
def view_rank_groups(data):

    if data is not None:

        children = []
        for (n, t) in data['Custom'].items():
            children.append(html.P('{}: {}'.format(n, ', '.join(list(t)))))
        
        return children
    
for i in range (0,11):
    @app.callback(
        Output(f'line_senderrank_main_{i}', 'options'),
        Input('user-rank-store', 'data'))
    def include_rank_groups_line(data):

        if data is not None:
            return data_parser.list_to_dash_option_dict(list(data_parser.get_rank_categories(data).keys()))
        return data_parser.list_to_dash_option_dict(list(data_parser.rank_categories.keys()))
    
@app.callback(
    Output('rank-main', 'options'),
    Input('user-rank-store', 'data'))
def include_rank_groups_topicmodel(data):

    if data is not None:
        return data_parser.list_to_dash_option_dict(list(data_parser.get_rank_categories(data).keys()))
    return data_parser.list_to_dash_option_dict(list(data_parser.rank_categories.keys()))
