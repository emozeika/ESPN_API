from extract import Extract
from mongoclient import MongoDBClient
from datetime import datetime




class ScoreBoardExtract:
    '''
    Extraction class to pull baseball data from ESPN
    '''
    ENDPOINT = 'games' 
    def __init__(self, league):
        self.LEAGUE = league


    def get_scoreboard(self, date = None):
        if not date:
            date = datetime.strftime(datetime.today(), "%Y%m%d")

        scoreboard = Extract().get_request(
                                            league = self.LEAGUE, 
                                            endpoint = self.ENDPOINT,
                                            filters = {'dates' : date}
                                        )

        return scoreboard
    
    def save_scoreboard(self, date = None, cluster = None):
        if not date:
            date = datetime.strftime(datetime.today(), "%Y%m%d")

        scoreboard = self.get_scoreboard(date)
        MongoDBClient(cluster).create_document(
                                        db_name = self.LEAGUE, 
                                        collection_name = self.ENDPOINT, 
                                        document_id = date, 
                                        content = scoreboard
                                    )



