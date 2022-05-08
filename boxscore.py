from extract import Extract
from mongoclient import MongoDBClient
from scoreboard import ScoreBoardExtract
from datetime import datetime
from pprint import pprint





class BoxScoreExtract:
    '''
    Extraction class to pull data from ESPN for box scores and send to Mongo DB 
    '''
    ENDPOINT = 'stats' 
    def __init__(self, league):
        self.LEAGUE = league
    
    def get_boxscore(self, event_id):
        '''
        Function to retrive the box score for a specific event. This returns the json type 
        data for the event parameter.
        '''
        box_score = Extract().get_request(
                                            league = self.LEAGUE, 
                                            endpoint = self.ENDPOINT,
                                            filters = {'event' : event_id}
                                        )

        return box_score


    def get_event_ids(self, date = None):
        '''
        Helper function to recieve all the event ids for a specific date. Returns 
        a list of event ids.
        '''
        scoreboard_data = ScoreBoardExtract(league = self.LEAGUE).get_scoreboard(date = date)['events']

        event_ids = []
        for i in range(len(scoreboard_data)):
            event_ids.append(scoreboard_data[i]['id'])

        return event_ids


    def save_boxscore(self, event_id, cluster = None):
        '''
        Function to save the boxscore data for a specific game. Using the helper function 
        GET_BOXSCORE to retrive data and then utilizes the MongoDBClient class to store data.
        '''
        
        #if single event_id then turn it into a list to have loop work
        if type(event_id) != list:
            event_id = [event_id]

        for i in range(len(event_id)):
            box_score = self.get_boxscore(event_id = event_id[i])
            MongoDBClient(cluster).create_document(
                                            db_name = self.LEAGUE,
                                            collection_name = self.ENDPOINT, 
                                            document_id = event_id[i], 
                                            content = box_score
                                        )
            
    
    def save_boxscores(self, date = None, cluster = None):
        '''
        Function to save  boxscore data for a specific date. Using the helper function 
        GET_EVENT_IDS to retrive data and then utilizes the MongoDBClient class to store data.
        '''
        event_ids = self.get_event_ids(date = date)
        self.save_boxscore(event_id = event_ids, cluster = cluster)






BoxScoreExtract('mlb').save_boxscores()