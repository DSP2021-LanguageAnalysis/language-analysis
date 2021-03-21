import base64
import datetime
import io
import dash_table
from dash.dependencies import ClientsideFunction, Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

from app import app

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return [html.Div([
        html.H5("File uploaded successfully"),
        html.H5("File name: {}".format(filename)),
        html.H5("Upload timestamp: {}".format(datetime.datetime.fromtimestamp(date)))
        # ,dash_table.DataTable(
        #     data=df.head().to_dict('records'),
        #     columns=[{'name': i, 'id': i} for i in df.columns]
        # )
        ])], df.to_json()


app.clientside_callback(
    """
    function(contents) {
        if (contents === undefined) {
            return '';
        }
        var content_string = contents.split(",")[1];
        var decoded = atob(content_string);
        alert("Data uploaded")
        return decoded;
    }
    """,
    Output('memory', 'data'),
    Input('upload-data', 'contents')
)


# @app.callback(Output('output-data-upload', 'children'),
#                 Output('memory', 'data'),
#                 Input('upload-data', 'contents'),
#                 State('upload-data', 'filename'),
#                 State('upload-data', 'last_modified'),
#                 State('memory', 'data'))
# def update_output(contents, filename, last_modified, data):
# #def update_output(list_of_contents):
#     if contents is None:
#         raise PreventUpdate
#     else:
#         print("Starting data parsing")
#         children, data = parse_contents(contents, filename, last_modified)
#         print("Done with data parsing")
#         return children, data