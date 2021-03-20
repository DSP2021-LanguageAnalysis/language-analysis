from bs4 import BeautifulSoup
import pandas as pd
import glob
import plotly.express as px
from app import cache

class DataParser():

    def __init__(self):
        return 

    #@cache.memoize()
    def get_word_counts(self, df):
        # Word count DataFrame
        word_counts = df.groupby(['ID', 'Year']).size().to_frame(name = 'WordCount').reset_index()
        return word_counts

    #@cache.memoize()
    def get_pos_counts(self, df):
        # POS counts for each letter
        pos_counts = df.groupby(['ID', 'Tags', 'Year', 'WordCount']).size().to_frame(name = 'PosCount').reset_index()
        pos_counts['PosCountNorm'] = pos_counts['PosCount']/pos_counts['WordCount']*100
        return pos_counts

    #@cache.memoize()
    def get_mfn_ratio(self, df):
        pos_counts = self.get_pos_counts(df)
        # Male/female noun ratio per year group
        nn1_MF = df.groupby(['ID', 'Tags', 'Year', 'WordCount', 'SenderSex']).size().to_frame(name = 'SenderSexCount').reset_index()
        nn1_MF['PosCountNorm'] = pos_counts['PosCount']/pos_counts['WordCount']
        nn1_MF = nn1_MF[nn1_MF['Tags'] == 'NN1']
        nn1_MF = nn1_MF.groupby(['Year', 'SenderSex']).mean().reset_index()
        nn1_MF = nn1_MF.drop(['WordCount','SenderSexCount'], axis=1)
        return nn1_MF
        
    #@cache.memoize()
    def get_mfn_tag(self, df):
        pos_counts = self.get_pos_counts(df)
        # Male/female noun ratio per tag
        tag_MF = df.groupby(['ID', 'Tags', 'Year', 'WordCount', 'SenderSex']).size().to_frame(name = 'SenderSexCount').reset_index()
        tag_MF['PosCountNorm'] = pos_counts['PosCount']/pos_counts['WordCount']*100
        return tag_MF

    #@cache.memoize()
    def get_nn1_count(self, df):
        pos_counts = self.get_pos_counts(df)
        # NN1 tag count per year
        nn1_counts = pos_counts[pos_counts['Tags'] == 'NN1']
        nn1_counts = nn1_counts.groupby(['Year']).mean().reset_index()
        return nn1_counts

    #@cache.memoize()
    def get_pos_list(self, df):
        pos_set = set(df['Tags'])
        pos_list = [{'label':tag, 'value':tag} for tag in pos_set]
        return pos_list

    #@cache.memoize()
    def get_rank(self, df):
        rank_set = set(df['SenderRank'])
        rank_list = [{'label':rank, 'value':rank} for rank in rank_set]
        return rank_set, rank_list

    #@cache.memoize()
    def get_wc_fig(self, df):
        word_counts = self.get_word_counts(df)
        # Get specific data needed for the visualisations
        wc_fig = px.scatter(word_counts, x="Year", y="WordCount", title='Word count for each letter in corpus')
        return wc_fig

    #@cache.memoize()
    def get_fm_fig(self, df):
        nn1_MF = self.get_mfn_ratio(df)
        fm_fig = px.bar(nn1_MF, x="Year", y="PosCountNorm", color='SenderSex', barmode='group')
        #pc_fig = px.line(nn1_counts, x="Year", y="PosCountNorm")
        return fm_fig