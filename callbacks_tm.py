import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
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
pos_tags = data_parser.get_pos_list()

# Callback for the slider element
@app.callback(
    Output('slider-output', 'children'), # Modified string with the years is passed to the Div-element
    Output('slider-values', 'value'), # Unmodified list of the selected years is passed to the next callback 
    Input('time-slider', 'value'))
def set_cities_options(selected_years):
    years = 'Selected period: {start} - {end}'.format(start=selected_years[0], end=selected_years[1])

    return years, selected_years

# Callback function for the topic model tab
@app.callback(
    Output('top-topics', 'data'),
    Output('top-topics', 'columns'),
    Output('letter-topics', 'data'),
    Output('letter-topics', 'columns'),
    Output('letters-per-topic', 'data'),
    Output('letters-per-topic', 'columns'),
    Output('pyldavis-vis', 'srcDoc'),
    Input('button', 'n_clicks'), # Only pressing the button initiates the function
    State('num-topics', 'value'), # Parameters given by the user are saved in State
    State('num-iter', 'value'),
    State('tags-filter', 'value'),
    State('gender-filter', 'value'),
    State('rank-filter', 'value'), 
    State('rel-filter', 'value'), 
    State('slider-values', 'value'),
    State('stopwords-filter','value'),
    State('alpha','value'),
    State('alpha_boolean', 'value'),
    State('eta', 'value'),
    State('eta_boolean', 'value'),
    State('userseed','value'), prevent_initial_call=True)
def model_params(clicks, topics, iterations, tags, gender, rank, rel, years, userstopwords, alpha, alpha_boolean, eta, eta_boolean, userseed):

    # Lists all triggered callbacks 
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    # Only runs the model training if the button has been clicked
    if 'button' in changed_id:

        # Non-filtered data
        data = df

        # Filters the data based on user's choices
        if len(tags) != len(pos_tags):
            data = tm.filter_by_tag(df, tags)
        if gender != 'A':
            data = tm.filter_by_sex(data, gender)
        if len(rank) != len(rank_set):
            data = tm.filter_by_rank(data, rank)
        if len(rel) != len(rel_set):
            data = tm.filter_by_rel(data, rel)
        if years[0] is not min(years_set) or years[1] is not max(years_set):
            data = tm.filter_by_time(data, years)
        #if len(userstopwords) != 0:
        #    data = tm.filter_by_userstopwords(data, userstopwords)

        # Data preprocessing for the LDA model 
        corpus, dictionary, docs, strings = tm.prepare_data(data, userstopwords)
        # Set alpha and eta according to selection
        if alpha_boolean == True:
            alpha = 'auto'
        if eta_boolean == True:
            eta = 'auto'    
        # Creates the LDA topic model
        model, top_topics = tm.train_lda(corpus, dictionary, topics, iterations, alpha, eta, userseed)

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

        return dataframe.to_dict('records'), cols, letters_for_topics.to_dict('records'), cols2, letters_per_topic.to_dict('records'), cols3, html_vis

    else:
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update          
