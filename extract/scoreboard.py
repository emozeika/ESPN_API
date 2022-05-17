from extract import Extract
from mongoclient import MongoDBClient
from datetime import datetime
import json
import os


class ScoreBoardExtract(Extract):
    '''
    Extraction class to pull baseball data from ESPN
    '''
    ENDPOINT = 'games' 
    def __init__(self, league):
        self.LEAGUE = league
        super().__init__()



    def get_scoreboard(self, date = None):
        if not date:
            date = datetime.strftime(datetime.today(), "%Y%m%d")

        scoreboard = self.get_request(
                                            league = self.LEAGUE, 
                                            endpoint = self.ENDPOINT,
                                            filters = {'dates' : date}
                                        )

        return scoreboard



    def initialize_document(self, id, cluster = None):
        MongoDBClient(cluster).create_document(
                                            db_name = self.LEAGUE, 
                                            collection_name = self.ENDPOINT, 
                                            document_id = id, 
                                            content = {}
                                            )
    



    def clean_scoreboard(self, scoreboard):
        #remove the array wrapper on leagues and remove calendar array in leagues list
        scoreboard['leagues'] = scoreboard['leagues'][0]
        del scoreboard['leagues']['calendar']

        #clean events
        cleaned_events = {}
        if len(scoreboard['events']) > 0:
            for i in range(len(scoreboard['events'])):
                cleaned_events[str(i)] = scoreboard['events'][i]
                cleaned_events[str(i)]['competitions'] = scoreboard['events'][i]['competitions'][0]
                
                competitors = {}
                for j in range(len(cleaned_events[str(i)]['competitions']['competitors'])):
                    competitors[str(j)] = cleaned_events[str(i)]['competitions']['competitors'][j]
                    del competitors[str(j)]['team']['links']
                    columns_to_delete = ['linescores', 'statistics', 'leaders', 'records']
                    for column in columns_to_delete:
                        if column in competitors[str(j)].keys():
                            del competitors[str(j)][column]
                
                cleaned_events[str(i)]['competitions']['competitors'] = competitors


                #delete unecessary columns in events
                del cleaned_events[str(i)]['links']

                #delete unecessary columns in competitions
                columns_to_delete = ['notes', 'broadcasts', 'geoBroadcasts', 'leaders']
                for column in columns_to_delete:
                    if column in cleaned_events[str(i)]['competitions'].keys():
                        del cleaned_events[str(i)]['competitions'][column]

                #delete unecessary columns in status
                if 'featuredAthletes' in  cleaned_events[str(i)]['competitions']['status'].keys():
                    del cleaned_events[str(i)]['competitions']['status']['featuredAthletes']



            

        scoreboard['events'] = cleaned_events

        

        return scoreboard

    
    def save_scoreboard(self, date = None, cluster = None, save_to_folder = False):
        if not date:
            date = datetime.strftime(datetime.today(), "%Y%m%d")
        
        scoreboard = self.get_scoreboard(date)
        #check if response had error
        if 'code' in scoreboard.keys():
            print(f'RESPONSE ERROR FOR {date}')
            return

        scoreboard = self.clean_scoreboard(scoreboard)
        if len(scoreboard['events']) > 0:
            if not save_to_folder:
                MongoDBClient(cluster).create_document(
                                            db_name = self.LEAGUE, 
                                            collection_name = self.ENDPOINT, 
                                            document_id = date, 
                                            content = scoreboard
                                            )
            else:
                wdir = 'data/raw/' + self.LEAGUE + '/' + self.ENDPOINT + '/'
                try:
                    os.remove(wdir + date + '.json')
                    print('REMOVING FILE TO REWRITE')
                except:
                    pass
                start_time = datetime.now()    
                with open(wdir + date + '.json', 'w') as fp:
                    json.dump(scoreboard, fp)
                fp.close()
                print(f'FILED {date} SAVED ... time to save: {datetime.now() - start_time} seconds')
        else:
            print(f"NO EVENTS FOR DATE {date}")



if __name__ == '__main__':
    ScoreBoardExtract('mlb').save_scoreboard(save_to_folder=True)
    print('finished')
            