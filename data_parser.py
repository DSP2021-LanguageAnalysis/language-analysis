from bs4 import BeautifulSoup
import pandas as pd
import glob
import plotly.express as px
import string
from pos_categories import pos_categories, pos_labels, pos_dittos
from attribute_categories import rank_categories, relationship_categories, relationship_labels

class DataParser():
    df = None
    db_person = pd.read_csv('TCEECE/metadata/database-person.txt', sep='\t', encoding='iso-8859-1')
    db_person = db_person.set_index('PersonCode')
    path_to_csv = 'TCEECE/data.csv'

    def __init__(self):
        try:
            self.df = pd.read_csv(self.path_to_csv, index_col=False)
        except:
            self.db_person = pd.read_csv('TCEECE/metadata/database-person.txt', sep='\t', encoding='iso-8859-1')
            self.db_person = self.db_person.set_index('PersonCode')
            self.db_letter = pd.read_csv('TCEECE/metadata//database-letter.txt', sep='\t', encoding='iso-8859-1')
            self.db_letter = self.db_letter.set_index('LetterID')

            self.df = self.letters_to_df()
            self.df.to_csv(self.path_to_csv, index=False)
        # Delete rows with missing data
        self.df = self.df.dropna(axis='index')
        self.pos_categories = pos_categories
        self.rank_categories = rank_categories
        self.pos_labels = pos_labels
        self.pos_dittos = pos_dittos
        self.relationship_categories = relationship_categories
        self.relationship_labels = relationship_labels
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
            if part[2] == '' or  part[2][0] in string.punctuation:
                continue
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
                'WordCount': [self.db_letter.loc[id, 'WordCount']] * len(pos)
                }
        
        # Creates a Pandas Dataframe from the dict
        df = pd.DataFrame(data) 
        
        return df

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

    def get_pos_list(self):

        df = self.df
        pos_set = set(df['Tags'])
        pos_list = [{'label':tag, 'value':tag} for tag in pos_set]

        return pos_list

    def get_word_list(self):

        df = self.df
        word_set = set(df['Words'].str.lower())
        word_list = [{'label':word, 'value':word} for word in word_set]

        return word_list

    def get_rank(self):

        df = self.df
        rank_set = set(df['SenderRank'])
        rank_list = [{'label':rank, 'value':rank} for rank in rank_set]

        return rank_set, rank_list

    def get_relationship(self):

        df = self.df
        rel_set = set(df['RelCode'])
        rel_list = [{'label':rel, 'value':rel} for rel in rel_set]

        return rel_set, rel_list

    def get_years(self):

        df = self.df
        year_set = set(df['Year'])

        return year_set

    def get_fm_fig(self):

        nn1_MF = self.get_mfn_ratio()
        fm_fig = px.bar(nn1_MF, x="Year", y="PosCountNorm", color='SenderSex', barmode='group')
        #pc_fig = px.line(nn1_counts, x="Year", y="PosCountNorm")

        return fm_fig

    def list_to_dash_option_dict(self, l):
        
        options = [{'label':item, 'value':item} for item in l]
        
        return options

    def dict_to_dash_options_with_hover(self, d):
        
        options = [{'label':k, 'value':k, 'title':', '.join(v)} for k,v in d.items()]
        
        return options

    def pos_options_with_hover(self, custom, main):

        l = self.get_pos_categories(custom)[main]
        options = [{'label':tag, 'value':tag, 'title':self.pos_labels[tag] + '\n' + ', '.join(self.pos_dittos[tag])} for tag in l]
        
        return options

    def get_pos_categories(self, custom):

        try:
            all_pos_categories = dict()
            all_pos_categories.update(self.pos_categories)
            all_pos_categories.update(custom)
            return all_pos_categories
        except Exception as e:

            return self.pos_categories

    def include_ditto_tags_to_pos_list(self, pos_list):

        final_list = []
        for tag in pos_list:
            final_list.extend(self.pos_dittos[tag])

        return final_list

    def get_name(self, ids):

        person = self.db_person
        senders = ids.to_frame()
        tmp = person[['FirstName','LastName']]
        names = senders.join(tmp, on='Sender').reset_index(drop=True)

        return names
