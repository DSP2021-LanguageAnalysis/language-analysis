import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app import app

layout3 = html.Div([
    dbc.Nav(
        className ='navbar navbar-expand-lg navbar-dark bg-primary', 
        children=[
            html.H1(className='navbar-brand', children='VARIENG: TCEECE corpus analysis'),
            dbc.NavItem(dbc.NavLink('Overview', active=True, href='/app/overview')),
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
                        html.H2("App Overview"),
                        dcc.Markdown('''
                        This app has been created by a group of students as part of a course in the Data Science Master’s Program at the University of Helsinki. 

                        The app was created for, and in collaboration with, the Research Unit for the Study of Variation, Contacts, and Change in English (VARIENG). It allows for the exploration of a corpus of historical letters using data science methods. 

                        The corpus featured in the app is part of the Corpora of Early English Correspondence (CEEC). [The Corpora of Early English Correspondence](https://varieng.helsinki.fi/CoRD/corpora/CEEC/) have been compiled to facilitate sociolinguistic research into the history of English. The letters have been sampled from published letter collections and digitized by the corpus team, and they are accompanied by metadata on the letters and the social background of the correspondents. 

                        In particular, the corpus featured in the app is the [Tagged Corpus of Early English Correspondence Extension (TCEECE)](https://varieng.helsinki.fi/CoRD/corpora/CEEC/tceece_doc.html), a standardized-spelling, part-of-speech tagged version of the 18th-century part of the corpus, which covers the years 1680-1800, with a few individual letters from earlier periods. The POS tagset used in this version is [CLAWS7](http://ucrel.lancs.ac.uk/claws7tags.html). 

                        The app has two sections. The first is the part of speech, or POS tag, visualisation section. Here there are two tabs, containing bar and line graphs, to give the user a general overview of the dataset. This section contains various options to filter, restrict and visualise the dataset to allow the user freedom in their exploration. 

                        The second part of the app is the topic model section. This allows the user to generate, using the latent dirichlet allocation algorithm, a chosen number of “topics” from the data set. When properly filtered and parameterized, this allows the user to see which topics dominated the discussion in the letters. The app gives a wide array of options, so that the user can adjust based on their own questions of interest.

                        Each section contains an instruction tab for guidance on how to utilise the various features. Aside from the POS tag and Topic Model sections, there is an “add custom groups” area  wherein the user can classify their own sets of attributes, used for filtering the data in the aforementioned sections of the app. 

                        Should you require further instruction or information about the methods and parameters used in the project, consult the [app github page for more detail](https://github.com/DSP2021-LanguageAnalysis/language-analysis). 
                            ''')
                        ])

                       
              ])

])
                                    
