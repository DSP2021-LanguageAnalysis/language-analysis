import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate

from app import app
import globals

data_parser = globals.data_parser


@app.callback(
    Output('user-browser-store', 'data'),
    Input('add_pos_group_button', 'n_clicks'),
    [State('pos_group_name', 'value')],
    [State('pos_group_tags', 'value')],
    State('user-browser-store', 'data'))
def add_pos_group(n_clicks, name, tags, data):
    
    if n_clicks > 0:
        if data is None:
            data = dict()
        tags = tags.split(';')
        data[name] = tags
    
    return data


@app.callback(
    Output('cust_pos_groups', 'children'),
    Input('user-browser-store', 'data'))
def view_pos_groups(data):

    if data is not None:
        children = []
        for (n, t) in data.items():
            children.append(html.P('{}: {}'.format(n, ', '.join(list(t)))))
        
        return children


for i in range (0,11):
    @app.callback(
        Output(f'pos_groups_dropdown_{i}_main', 'options'),
        Input('user-browser-store', 'data'))
    def include_pos_groups_line(data):

        if data is not None:
            return data_parser.list_to_dash_option_dict(list(data_parser.get_pos_categories(data).keys()))
        return data_parser.list_to_dash_option_dict(list(data_parser.pos_categories.keys()))

@app.callback(
    Output('pos_tm_main', 'options'),
    Input('user-browser-store', 'data'))
def include_pos_groups_topicmodel(data):

    if data is not None:
        return data_parser.list_to_dash_option_dict(list(data_parser.get_pos_categories(data).keys()))
    return data_parser.list_to_dash_option_dict(list(data_parser.pos_categories.keys()))
