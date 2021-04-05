from bs4 import BeautifulSoup
import pandas as pd
import glob
import plotly.express as px
from zipfile import ZipFile

class DataParser():

    def __init__(self):
        column_types = {
            'ID': 'object',
            'Words': 'object',
            'Tags': 'object',
            'Year': 'uint16',
            'Sender': 'object',
            'SenderRank': 'object',
            'SenderSex': 'object',
            'RelCode': 'object',
            'WordCount': 'uint16'
        }

        with ZipFile('data/full_data.zip') as zip:
            data = zip.open('full_data.csv')

        self.frame = pd.read_csv(data, dtype=column_types)

        self.pos_counts = self.frame.groupby(['ID', 'Tags', 'Year', 'WordCount']).size().to_frame(name = 'PosCount').reset_index()
        self.pos_counts['PosCountNorm'] = self.pos_counts['PosCount']/self.pos_counts['WordCount']*100

        self.word_counts = self.frame.groupby(['ID', 'Year']).size().to_frame(name = 'WordCount').reset_index()

        return 
        
    def letters_to_df(self):
        return self.frame

    def get_word_counts(self):
        return self.word_counts

    def get_pos_counts(self):

        df = self.letters_to_df()
        # POS counts for each letter
        pos_counts = df.groupby(['ID', 'Tags', 'Year', 'WordCount']).size().to_frame(name = 'PosCount').reset_index()
        pos_counts['PosCountNorm'] = pos_counts['PosCount']/pos_counts['WordCount']*100

        return pos_counts

    def get_mfn_ratio(self):

        df = self.letters_to_df()
        pos_counts = self.get_pos_counts()
        # Male/female noun ratio per year group
        nn1_MF = df.groupby(['ID', 'Tags', 'Year', 'WordCount', 'SenderSex']).size().to_frame(name = 'SenderSexCount').reset_index()
        nn1_MF['PosCountNorm'] = pos_counts['PosCount']/pos_counts['WordCount']
        nn1_MF = nn1_MF[nn1_MF['Tags'] == 'NN1']
        nn1_MF = nn1_MF.groupby(['Year', 'SenderSex']).mean().reset_index()
        nn1_MF = nn1_MF.drop(['WordCount','SenderSexCount'], axis=1)
        #app.logger.info(nn1_MF)

        return nn1_MF
        
    def get_mfn_tag(self):

        df = self.letters_to_df()
        pos_counts = self.get_pos_counts()
        # Male/female noun ratio per tag
        tag_MF = df.groupby(['ID', 'Tags', 'Year', 'WordCount', 'SenderSex']).size().to_frame(name = 'SenderSexCount').reset_index()
        tag_MF['PosCountNorm'] = pos_counts['PosCount']/pos_counts['WordCount']*100

        return tag_MF

    def get_nn1_count(self):

        pos_counts = self.get_pos_counts()
        # NN1 tag count per year
        nn1_counts = pos_counts[pos_counts['Tags'] == 'NN1']
        nn1_counts = nn1_counts.groupby(['Year']).mean().reset_index()

        return nn1_counts

    def get_pos_list(self):

        df = self.letters_to_df()
        pos_set = set(df['Tags'])
        pos_list = [{'label':tag, 'value':tag} for tag in pos_set]

        return pos_list

    def get_rank(self):

        df = self.letters_to_df()
        rank_set = set(df['SenderRank'])
        rank_list = [{'label':rank, 'value':rank} for rank in rank_set]

        return rank_set, rank_list

    def get_relationship(self):

        df = self.letters_to_df()
        rel_set = set(df['RelCode'])
        rel_list = [{'label':rel, 'value':rel} for rel in rel_set]

        return rel_set, rel_list

    def get_years(self):

        df = self.letters_to_df()
        year_set = set(df['Year'])

        return year_set

    def get_wc_fig(self):

        word_counts = self.get_word_counts()
        # Get specific data needed for the visualisations
        wc_fig = px.scatter(word_counts, x="Year", y="WordCount", title='Word count for each letter in corpus')

        return wc_fig

    def get_fm_fig(self):

        nn1_MF = self.get_mfn_ratio()
        fm_fig = px.bar(nn1_MF, x="Year", y="PosCountNorm", color='SenderSex', barmode='group')
        #pc_fig = px.line(nn1_counts, x="Year", y="PosCountNorm")

        return fm_fig