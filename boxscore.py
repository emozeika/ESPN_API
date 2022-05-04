from extract import Extract
from mongoclient import MongoDBClient
from datetime import datetime






class BoxScoreExtract:
    '''
    Extraction class to pull baseball data from ESPN
    '''
    ENDPOINT = 'stats' 
    def __init__(self, league):
        self.LEAGUE = league
    
    def get_boxscore(self, event_id):
        box_score = Extract().get_request(
                                            league = self.LEAGUE, 
                                            endpoint = self.ENDPOINT,
                                            filters = {'event' : event_id}
                                        )

        return box_score
    

    def save_boxscore(self, event_id):

        box_score = self.get_boxscore(event_id)
        MongoDBClient().create_document(
                                        db_name = self.LEAGUE,
                                        collection_name = self.ENDPOINT, 
                                        document_id = event_id, 
                                        content = box_score
        
                                    )



BoxScoreExtract('mlb').save_boxscore('401355603')