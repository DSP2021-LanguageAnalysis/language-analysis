import pandas as pd
import numpy as np
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from gensim.corpora import Dictionary
from gensim.models import LdaModel

def prepare_data(data):
    
    # Group the data by the letter id and concatenate words from each letter to one string
    strings = data.groupby('ID').agg(lambda col: ' '.join(col))

    # Create a list of strings of the letters for Gensim
    docs = list(strings['Words'])
    
    # Split the documents into tokens.
    tokenizer = RegexpTokenizer(r'\w+')
    
    for idx in range(len(docs)):
        docs[idx] = docs[idx].lower()  # Convert to lowercase.
        docs[idx] = tokenizer.tokenize(docs[idx])  # Split into words.

    # Remove numbers, but not words that contain numbers.
    docs = [[token for token in doc if not token.isnumeric()] for doc in docs]

    # Remove words that are only one character.
    docs = [[token for token in doc if len(token) > 1] for doc in docs]
    
    # Lemmatize the documents.
    lemmatizer = WordNetLemmatizer()
    docs = [[lemmatizer.lemmatize(token) for token in doc] for doc in docs]
    
    # Create a dictionary representation of the documents.
    dictionary = Dictionary(docs)

    # Filter out words that occur less than 10 documents, or more than 50% of the documents.
    #dictionary.filter_extremes(no_below=10, no_above=0.5)
    
    # Bag-of-words representation of the documents.
    corpus = [dictionary.doc2bow(doc) for doc in docs]
    
    return corpus, dictionary, docs

# Filter the data based on the POS tags 
def filter_by_tag(data, tags):
    tag_data = data.loc[data['Tags'].isin(tags)]
    
    return tag_data

# Filter the data based on the gender of the author
def filter_by_sex(data, sex):
    gender_data = data.loc[data['SenderSex'] == sex]
    
    return gender_data

# Filter the data based on the rank of the author
def filter_by_rank(data, rank):
    rank_data = data.loc[data['SenderRank'].isin(rank)]
    
    return rank_data

# Train the LDA topic model
def train_lda(data, dictionary, n_topics, n_iter):
    
    # Set training parameters.
    num_topics = n_topics
    chunksize = 1000
    passes = 1
    iterations = n_iter
    eval_every = None  
    # Set random seed
    random_seed = 135
    state = np.random.RandomState(random_seed)


    # Train LDA model.
    model = LdaModel(
        corpus=data,
        id2word=dictionary,
        chunksize=chunksize,
        alpha='auto',
        eta='auto',
        iterations=iterations,
        num_topics=num_topics,
        passes=passes,
        eval_every=eval_every,
        random_state=state
    )
    
    top_topics = model.top_topics(data)
    
    return model, top_topics