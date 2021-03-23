from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash import no_update
import pandas as pd
import pyLDAvis
import pyLDAvis.gensim

from app import app
from topic_model import TopicModel
from data_parser import DataParser

data_parser = DataParser()
tm = TopicModel()
df = data_parser.letters_to_df()
pos_counts = data_parser.get_pos_counts()
rank_set, rank_list = data_parser.get_rank()
rel_set, rel_list = data_parser.get_relationship()
years_set = data_parser.get_years()

# Callback function for the topic model tab
@app.callback(
    Output('top-topics', 'data'),
    Output('top-topics', 'columns'),
    Output('letter-topics', 'data'),
    Output('letter-topics', 'columns'),
    Output('letters-per-topic', 'data'),
    Output('letters-per-topic', 'columns'),
    Output('pyldavis-vis', 'srcDoc'),
    Output('slider-output', 'children'),
    Input('button', 'n_clicks'), # Only pressing the button initiates the function
    Input('time-slider', 'value'),
    State('num-topics', 'value'), # Parameters given by the user are saved in State
    State('num-iter', 'value'),
    State('tags-filter', 'value'),
    State('gender-filter', 'value'),
    State('rank-filter', 'value'), 
    State('rel-filter', 'value'), prevent_initial_call=True)
def model_params(clicks, time, topics, iterations, tags, gender, rank, rel):

    years = 'Selected period: {start} - {end}'.format(start=time[0], end=time[1])

    if clicks > 0:

        # Uses the functions imported from topic_model.py
        data = tm.filter_by_tag(df, tags)
        if gender != 'A':
            data = tm.filter_by_sex(data, gender)
        if len(rank) != len(rank_set):
            data = tm.filter_by_rank(data, rank)
        if len(rel) != len(rel_set):
            data = tm.filter_by_rel(data, rel)
        if time[0] is not min(years_set) or time[1] is not max(years_set):
            data = tm.filter_by_time(data, time)
        # Data preprocessing for the LDA model 
        corpus, dictionary, docs, strings = tm.prepare_data(data)
        # Creates the LDA topic model
        model, top_topics = tm.train_lda(corpus, dictionary, topics, iterations)

        dominant_topics = tm.letter_topics(model, corpus, strings)

        letters_for_topics = tm.get_most_representative(dominant_topics)

        letters_per_topic = tm.letters_per_topic(dominant_topics)

        # Loop that creates a dataframe from the LDA top topics list
        i=1
        i=1
        topic_dict = {}
        for topic in top_topics:
            entries = []
            for t in topic[0]:
                score = round(float(t[0]), 3)
                tmp = t[1]+', '+ str(score)
                entries.append(tmp)
            topic_dict['Topic {}'.format(i)] =  entries       
            i += 1

        dataframe = pd.DataFrame(topic_dict)
        cols = [{"name": i, "id": i} for i in dataframe.columns]
        cols2 = [{"name": i, "id": i} for i in letters_for_topics.columns[1:]]
        cols3 = [{"name": i, "id": i} for i in letters_per_topic.columns[1:]]

        # Creates the pyLDAvis visualisation of the LDA model
        vis_data = pyLDAvis.gensim.prepare(model, corpus, dictionary)
        html_vis = pyLDAvis.prepared_data_to_html(vis_data, template_type='general')

        return dataframe.to_dict('records'), cols, letters_for_topics.to_dict('records'), cols2, letters_per_topic.to_dict('records'), cols3, html_vis, years

    else:
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, years           