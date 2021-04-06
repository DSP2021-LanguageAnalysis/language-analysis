from data_parser import DataParser
from topic_model import TopicModel

def initialize(): 
    global data_parser
    data_parser = DataParser() 

    global topic_model
    topic_model = TopicModel() 