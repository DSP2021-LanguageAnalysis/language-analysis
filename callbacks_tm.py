import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash import no_update
from dash.exceptions import PreventUpdate
import pandas as pd
import pyLDAvis
import pyLDAvis.gensim

from app import app
import globals

tm = globals.topic_model
data_parser = globals.data_parser
df = data_parser.df
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

@app.callback(
    Output('letter-scores', 'data'), 
    Output('letter-scores', 'columns'), 
    Input('button2', 'n_clicks'),
    State('letter-list', 'value'), prevent_initial_call=True)
def set_letter_topics(clicks,indices):
    if indices:
        letter_topics = tm.get_letter_topics(indices)
        cols = [{"name": i, "id": i} for i in letter_topics.columns]

        return letter_topics.to_dict('records'), cols
    else:
        return None, None


# Callback function for the topic model tab
@app.callback(
    Output('top-topics', 'data'),
    Output('top-topics', 'columns'),
    Output('letter-topics', 'data'),
    Output('letter-topics', 'columns'),
    Output('letters-per-topic', 'data'),
    Output('letters-per-topic', 'columns'),
    Output('pyldavis-vis', 'srcDoc'),
    Output('letter-list','options'),
    Output('tm-results','hidden'),
    Input('button', 'n_clicks'), # Only pressing the button initiates the function
    Input('alpha_boolean', 'on'),
    Input('eta_boolean', 'on'),
    State('num-topics', 'value'), # Parameters given by the user are saved in State
    State('num-iter', 'value'),
    State('tags-filter', 'value'),
    State('gender-filter', 'value'),
    State('rank-filter', 'value'), 
    State('rel-filter', 'value'), 
    State('slider-values', 'value'),
    State('stopwords-filter','value'),
    State('alpha','value'),
    State('eta', 'value'),
    State('userseed','value'), prevent_initial_call=True)
def model_params(clicks, alpha_boolean, eta_boolean, topics, iterations, tags, gender, rank, rel, years, userstopwords, alpha, eta, userseed):

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

        # Data preprocessing for the LDA model 
        corpus, dictionary, docs, strings = tm.prepare_data(data, userstopwords)
   
        # Creates the LDA topic model
        model = tm.train_lda(corpus, dictionary, topics, iterations, alpha, alpha_boolean, eta, eta_boolean, userseed)

        # Gets the top 20 words for each topic
        topics_df = tm.get_topics()

        dominant_topics = tm.letter_topics()

        letters_for_topics = tm.get_most_representative(dominant_topics)

        letters_per_topic = tm.letters_per_topic(dominant_topics)

        letter_list = tm.get_letter_list()

        cols = [{"name": i, "id": i} for i in topics_df.columns]
        cols2 = [{"name": i, "id": i} for i in letters_for_topics.columns]
        cols3 = [{"name": i, "id": i} for i in letters_per_topic.columns]

        # Creates the pyLDAvis visualisation of the LDA model
        vis_data = pyLDAvis.gensim.prepare(model, corpus, dictionary)
        html_vis = pyLDAvis.prepared_data_to_html(vis_data, template_type='general')

        return topics_df.to_dict('records'), cols, letters_for_topics.to_dict('records'), cols2, letters_per_topic.to_dict('records'), cols3, html_vis, letter_list, False

    else:
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, True          
