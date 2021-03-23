from bs4 import BeautifulSoup
import pandas as pd
import glob
import plotly.express as px
from app import cache

class DataParser():

    def __init__(self):
        self.db_person = pd.read_csv('TCEECE/metadata/database-person.txt', sep='\t', encoding='iso-8859-1')
        self.db_person = self.db_person.set_index('PersonCode')
        self.db_letter = pd.read_csv('TCEECE/metadata//database-letter.txt', sep='\t', encoding='iso-8859-1')
        self.db_letter = self.db_letter.set_index('LetterID')
        return 
        
    # Transforms xml-file into a BeautifulSoup-object
    def read_tei(self, tei_file):
        with open(tei_file, 'r') as tei:
            soup = BeautifulSoup(tei, 'lxml')
            return soup
        raise RuntimeError('Cannot generate a soup from the input')

    # Creates a Pandas dataframe from a letter specified by the path-argument 
    # with letted id, words and corresponding POS-tags as the columns 
    def parse_letter(self, path):
        lst = []
        pos = []
        words = []
        
        # Creates a BeautifulSoup-object
        soup = self.read_tei(path)
        
        # Locates the letter text by using the p-tags and extracts it into a list 
        text = list(soup.find_all('p'))
        
        # Splits the text into single items (word+POS-tag) and adds them to a list
        for item in text:
            lst += item.text.split()
        
        # Splits the items into POS-tags and words and adds them to separate lists
        for item in lst:
            part = item.partition("_")
            pos.append(part[2])
            words.append(part[0])

        # Extracts the id of the letter from the TEI-tag
        id = soup.tei.attrs['xml:id']
        sender = self.db_letter.loc[id, 'Sender']
        
        # Combines the lists into a dict. The id is repeated for each word 
        data = {'ID': [id] * len(pos),
                'Words':words, 
                'Tags':pos,
                'Year': [self.db_letter.loc[id, 'Year']] * len(pos),
                'Sender': [self.db_letter.loc[id, 'Sender']] * len(pos), 
                'SenderRank': [self.db_letter.loc[id, 'SenderRank']] * len(pos),
                'SenderSex': [self.db_person.loc[sender, 'Sex']] *len(pos),
                'RelCode': [self.db_letter.loc[id, 'RelCode']] * len(pos),
                'WordCount': [len(words)] * len(words)
                }
        
        # Creates a Pandas Dataframe from the dict
        df = pd.DataFrame(data) 
        
        return df

    @cache.memoize()
    def letters_to_df(self):
        # Path of the folder where the letters are located (change path to correct location when using this)
        path = 'TCEECE/tceece-letters-c7' 

        # Uses glob-library to create a list of all the .txt-files in the folder
        all_files = glob.glob(path + "/*.txt")

        li = []

        # Creates separate dataframes from each letter and adds them to a list
        for filename in all_files:
            df = self.parse_letter(filename)
            li.append(df)

        # Combines all dataframes in the list by using the concat-method of Pandas
        frame = pd.concat(li, axis=0, ignore_index=True)

        return frame

    @cache.memoize()
    def get_word_counts(self):

        df = self.letters_to_df()
        # Word count DataFrame
        word_counts = df.groupby(['ID', 'Year']).size().to_frame(name = 'WordCount').reset_index()

        return word_counts

    @cache.memoize()
    def get_pos_counts(self):

        df = self.letters_to_df()
        # POS counts for each letter
        pos_counts = df.groupby(['ID', 'Tags', 'Year', 'WordCount']).size().to_frame(name = 'PosCount').reset_index()
        pos_counts['PosCountNorm'] = pos_counts['PosCount']/pos_counts['WordCount']*100

        return pos_counts

    @cache.memoize()
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
        
    @cache.memoize()
    def get_mfn_tag(self):

        df = self.letters_to_df()
        pos_counts = self.get_pos_counts()
        # Male/female noun ratio per tag
        tag_MF = df.groupby(['ID', 'Tags', 'Year', 'WordCount', 'SenderSex']).size().to_frame(name = 'SenderSexCount').reset_index()
        tag_MF['PosCountNorm'] = pos_counts['PosCount']/pos_counts['WordCount']*100

        return tag_MF

    @cache.memoize()
    def get_nn1_count(self):

        pos_counts = self.get_pos_counts()
        # NN1 tag count per year
        nn1_counts = pos_counts[pos_counts['Tags'] == 'NN1']
        nn1_counts = nn1_counts.groupby(['Year']).mean().reset_index()

        return nn1_counts

    @cache.memoize()
    def get_pos_list(self):

        df = self.letters_to_df()
        pos_set = set(df['Tags'])
        pos_list = [{'label':tag, 'value':tag} for tag in pos_set]

        return pos_list

    @cache.memoize()
    def get_rank(self):

        df = self.letters_to_df()
        rank_set = set(df['SenderRank'])
        rank_list = [{'label':rank, 'value':rank} for rank in rank_set]

        return rank_set, rank_list

    @cache.memoize()
    def get_relationship(self):

        df = self.letters_to_df()
        rel_set = set(df['RelCode'])
        rel_list = [{'label':rel, 'value':rel} for rel in rel_set]

        return rel_set, rel_list

    @cache.memoize()
    def get_years(self):

        df = self.letters_to_df()
        year_set = set(df['Year'])

        return year_set

    @cache.memoize()
    def get_wc_fig(self):

        word_counts = self.get_word_counts()
        # Get specific data needed for the visualisations
        wc_fig = px.scatter(word_counts, x="Year", y="WordCount", title='Word count for each letter in corpus')

        return wc_fig

    @cache.memoize()
    def get_fm_fig(self):

        nn1_MF = self.get_mfn_ratio()
        fm_fig = px.bar(nn1_MF, x="Year", y="PosCountNorm", color='SenderSex', barmode='group')
        #pc_fig = px.line(nn1_counts, x="Year", y="PosCountNorm")

        return fm_fig