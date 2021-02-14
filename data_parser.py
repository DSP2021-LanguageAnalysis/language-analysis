from bs4 import BeautifulSoup
import pandas as pd
import glob

class DataParser():

    def __init__(self):
        self.db_person = pd.read_csv('TCEECE/metadata/database-person.txt', sep='\t')
        self.db_person = self.db_person.set_index('PersonCode')
        self.db_letter = pd.read_csv('TCEECE/metadata//database-letter.txt', sep='\t')
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
        
        # Combines the lists into a dict. The id is repeated for each word 
        data = {'ID': [id] * len(pos),
                'Words':words, 
                'Tags':pos,
                'Year': [self.db_letter.loc[id, 'Year']] * len(pos)}
        
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