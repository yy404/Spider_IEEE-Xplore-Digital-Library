from items import Paper
import pymongo
from pymongo import IndexModel, ASCENDING


class IeeexplorePipeline(object):
    def __init__(self):
    	client = pymongo.MongoClient("localhost", 27017)
    	db = client['IEEE']

    	self.term_paper_table["paper_table"]
    	idx = IndexModel([('ID', ASCENDING)], unique=True)
    	self.term_paper_table.create_indexes([idx])

    
