import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash import no_update
from dash.exceptions import PreventUpdate
import pandas as pd
from pandas.core.common import flatten
import pyLDAvis
import pyLDAvis.gensim

from app import app
import globals

tm = globals.topic_model
data_parser = globals.data_parser
df = data_parser.df
rank_set, rank_list = data_parser.get_rank()
rel_set, rel_list = data_parser.get_relationship()
years_set = data_parser.get_years()
pos_tags = data_parser.get_pos_list()

# Callback for the POS tag selector
@app.callback(
    Output('pos_tm_sub', 'value'),
    Output('pos_tm_sub', 'options'),
    [Input('pos_tm_main', 'value')],
    State('user-pos-store', 'data'))
def tm_pos_options(mains, data):
    values = []
    options = []
    for main in mains:
        value = data_parser.get_pos_categories(data)[main]
        values.extend(value)
        options.extend(data_parser.list_to_dash_option_dict(value))

    return values, options

# Callback for the rank filter selector
@app.callback(
    Output('rank-sub', 'value'),
    Output('rank-sub', 'options'),
    Input('rank-main', 'value'),
    State('user-pos-store', 'data'))
def tm_rank_options(main, data):

    values = []
    options = []
    value = list(data_parser.rank_categories[main].keys())
    values.extend(value)
    options.extend(data_parser.dict_to_dash_options_with_hover(data_parser.rank_categories[main]))
        
    return values, options

# Callback for the relationship filter selector
@app.callback(
    Output('relationship-sub', 'value'),
    Output('relationship-sub', 'options'),
    Input('relationship-main', 'value'),
    State('user-relationship-store', 'data'))
def tm_rel_options(main, data):

    values = []
    options = []
    value = list(data_parser.get_rel_categories(data)[main].keys())
    values.extend(value)
    options.extend(data_parser.dict_to_dash_options_with_hover(data_parser.get_rel_categories(data)[main]))
        
    return values, options

# Callback for the slider element
@app.callback(
    Output('slider-output', 'children'), # Modified string with the years is passed to the Div-element
    Output('slider-values', 'value'), # Unmodified list of the selected years is passed to the next callback 
    Input('time-slider', 'value'))
def set_years(selected_years):
    years = 'Selected period: {start} - {end}'.format(start=selected_years[0], end=selected_years[1])

    return years, selected_years

# Callback for the letter selector
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

# Callback for the topic selector and data table
@app.callback(
    Output('letter-topics', 'data'),
    Output('letter-topics', 'columns'),
    Input('topic-selector', 'value'), prevent_initial_call=True)
def get_letters_per_topic(topic_id):
    letters_for_topic = tm.get_topic_letters(topic_id)
    letters_for_topic = letters_for_topic.drop(columns=['Topic'])
    cols = [{"name": i, "id": i} for i in letters_for_topic.columns]

    return letters_for_topic.to_dict('records'), cols


# Callback function for the topic model tab
@app.callback(
    Output('corpus_size_info', 'children'),
    Output('top-topics', 'data'),
    Output('top-topics', 'columns'),
    Output('topic-selector', 'options'),
    Output('letters-per-topic', 'data'),
    Output('letters-per-topic', 'columns'),
    Output('pyldavis-vis', 'srcDoc'),
    Output('letter-list','options'),
    Output('tm-results','hidden'),
    Output('confirm', 'displayed'),
    Input('button', 'n_clicks'), # Only pressing the button initiates the function
    State('alpha_boolean', 'on'),
    State('eta_boolean', 'on'),
    State('num-topics', 'value'), # Parameters given by the user are saved in State
    State('num-iter', 'value'),
    State('pos_tm_sub', 'value'),
    State('gender-filter', 'value'),
    State('rank-main', 'value'),
    State('rank-sub', 'value'), 
    State('relationship-main', 'value'),
    State('relationship-sub', 'value'), 
    State('slider-values', 'value'),
    State('stopwords-filter','value'),
    State('alpha','value'),
    State('eta', 'value'),
    State('userseed','value'), 
    State('filter-low','value'),
    State('filter-high','value'),
    State('user-relationship-store', 'data'), prevent_initial_call=True)
def model_params(clicks, alpha_boolean, eta_boolean, topics, iterations, tags, gender, rank_main, rank_sub, rel_main, rel_sub, years, userstopwords, alpha, eta, userseed, min_doc, max_prop, custom_rel):

    # Lists all triggered callbacks 
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    # Only runs the model training if the button has been clicked
    if 'button' in changed_id:

        # Non-filtered data
        data = df

        # Filters the data based on user's choices

        # Filtering by selected POS-tags
        data = tm.filter_by_tag(df, tags)
        # Filtering by selected ranks
        ranks = list(flatten([data_parser.rank_categories[rank_main][sub] for sub in rank_sub]))
        data = tm.filter_by_rank(data, ranks)
        # Filtering by selected relationship tags
        relationships = list(flatten([data_parser.get_rel_categories(custom_rel)[rel_main][rel_sub] for rel_sub in rel_sub]))
        data = tm.filter_by_rel(data, relationships)
        # Filtering by gender
        if gender != 'A':
            data = tm.filter_by_sex(data, gender)
        # Filtering by selected time period
        if years[0] is not min(years_set) or years[1] is not max(years_set):
            data = tm.filter_by_time(data, years)

        # Gives a message to user if the dataframe is empty after filtering
        if(data.empty):
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, True, True 

        # Data preprocessing for the LDA model 
        corpus, dictionary, docs, strings = tm.prepare_data(data, userstopwords, min_doc, max_prop)
   
        # Creates the LDA topic model
        model = tm.train_lda(corpus, dictionary, topics, iterations, alpha, alpha_boolean, eta, eta_boolean, userseed)

        # Gets the top 20 words for each topic and topic list for the dropdown
        topics_df, topic_list = tm.get_topics()

        dominant_topics = tm.letter_topics()

        letters_per_topic = tm.letters_per_topic(dominant_topics)

        tm.get_most_representative(dominant_topics)

        letter_list = tm.get_letter_list()

        cols = [{"name": i, "id": i} for i in topics_df.columns]
        cols2 = [{"name": i, "id": i} for i in letters_per_topic.columns]

        # Creates the pyLDAvis visualisation of the LDA model
        vis_data = pyLDAvis.gensim.prepare(model, corpus, dictionary, sort_topics=False)
        html_vis = pyLDAvis.prepared_data_to_html(vis_data, template_type='general')

        corpus_size_msg = f"Corpus size after filtering: {dictionary.num_docs} letters, {dictionary.num_pos} (non-unique) words processed"
        
        return corpus_size_msg, topics_df.to_dict('records'), cols, topic_list, letters_per_topic.to_dict('records'), cols2, html_vis, letter_list, False, False

    else:
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, True, False          
