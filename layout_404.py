import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app import app

layout404 = html.Div([
    dbc.Nav(
        className ='navbar navbar-expand-lg navbar-dark bg-primary', 
        children=[
            html.H1(className='navbar-brand', children='VARIENG: TCEECE corpus analysis'),
            dbc.NavItem(dbc.NavLink('Overview', href='/app/overview')),
            dbc.NavItem(dbc.NavLink('POS tag analysis', href='/app/postags')),
            dbc.NavItem(dbc.NavLink('Topic model', href='/app/topicmodel')),
            dbc.NavItem(dbc.NavLink('Add custom groups', href='/app/customize'))
        ],
        pills=True
    ),
    html.Div(children=[
                html.Div(
                    style={'padding': '20px'},
                    children=[
                        html.H2("404"),
                        dcc.Markdown('''
                            Nothing in this path, choose destination from the links above.                        
                            ''')
                        ])

                       
              ])

])
                                    
