from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash import no_update
import pandas as pd
import pyLDAvis
import pyLDAvis.gensim

from app import app
from topic_model import prepare_data, filter_by_tag, train_lda, filter_by_sex, filter_by_rank
from data_parser import DataParser

data_parser = DataParser()
df = data_parser.letters_to_df()
pos_counts = data_parser.get_pos_counts()
rank_set, rank_list = data_parser.get_rank()

# Callback function for the topic model tab
@app.callback(
    Output('top-topics', 'data'),
    Output('top-topics', 'columns'),
    Output('pyldavis-vis', 'srcDoc'),
    Input('button', 'n_clicks'), # Only pressing the button initiates the function
    State('num-topics', 'value'), # Parameters given by the user are saved in State
    State('num-iter', 'value'),
    State('tags-filter', 'value'),
    State('gender-filter', 'value'),
    State('rank-filter', 'value'), prevent_initial_call=True)
def model_params(clicks, topics, iterations, tags, gender, rank):

    if clicks > 0:

        # Uses the functions imported from topic_model.py
        data = filter_by_tag(df, tags)
        if gender != 'A':
            data = filter_by_sex(data, gender)
        if len(rank) != len(rank_set):
            data = filter_by_rank(data, rank)
        # Data preprocessing for the LDA model 
        corpus, dictionary, docs = prepare_data(data)
        # Creates the LDA topic model
        model, top_topics = train_lda(corpus, dictionary, topics, iterations)

        # Loop that creates a dataframe from the LDA top topics list
        i=1
        topic_dict = {}
        for topic in top_topics:
            words = []
            scores = []
            for t in topic[0]:
                words.append(t[1])
                scores.append(t[0])
            topic_dict['Topic {}: words'.format(i)] =  words 
            topic_dict['Topic {}: scores'.format(i)] = scores            
            i += 1

        dataframe = pd.DataFrame(topic_dict)
        cols = [{"name": i, "id": i} for i in dataframe.columns]

        # Creates the pyLDAvis visualisation of the LDA model
        vis_data = pyLDAvis.gensim.prepare(model, corpus, dictionary)
        html_vis = pyLDAvis.prepared_data_to_html(vis_data, template_type='general')

        return dataframe.to_dict('records'), cols, html_vis

    else:
        return no_update, no_update, no_update         