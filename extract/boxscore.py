from extract import Extract
from mongoclient import MongoDBClient
from scoreboard import ScoreBoardExtract
from datetime import datetime
import os
import json





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
        start_time = datetime.now()
        box_score = Extract().get_request(
                                            league = self.LEAGUE, 
                                            endpoint = self.ENDPOINT,
                                            filters = {'event' : event_id}
                                        )
        #print(f"RETRIEVED DATA... time to retrieve {datetime.now() - start_time}")
        return box_score


    def clean_game_officials(self, box_score):
        if 'gameInfo' in box_score.keys():
            if 'officials' in box_score['gameInfo'].keys():
                officials = {}
                for i in range(len(box_score['gameInfo']['officials'])):
                    officials[str(i)] = box_score['gameInfo']['officials'][i]
                box_score['gameInfo']['officials'] = officials

        return box_score
                

    def transform_plays(self, box_score):
        if 'plays' in box_score.keys():
            plays = {}
            for i in range(len(box_score['plays'])):
                plays[str(i)] = box_score['plays'][i]
            box_score['plays'] = plays
        
        return box_score
    

    def clean_pickcenter(self, box_score):
        if 'pickcenter' in box_score.keys():
            pickcenter = {}
            for i in range(len(box_score['pickcenter'])):
                pickcenter[str(i)] = box_score['pickcenter'][i]
                if 'links' in pickcenter[str(i)].keys():
                    del pickcenter[str(i)]['links']
            box_score['pickcenter'] = pickcenter

        return box_score


    def clean_header(self, box_score):
        #removing all unecessary tabs
        if 'header' in box_score.keys():
            if 'links' in box_score['header'].keys():
                del box_score['header']['links']
            if 'links' in box_score['header']['league'].keys():
                del box_score['header']['league']['links']
            if 'competitions' in box_score['header'].keys():
                box_score['header']['competitions'] = box_score['header']['competitions'][0]
                for column in ['broadcasts', 'series']:
                    if column in box_score['header']['competitions'].keys():
                        del box_score['header']['competitions'][column]
                if 'featuredAthletes' in box_score['header']['competitions']['status'].keys():
                    del box_score['header']['competitions']['status']['featuredAthletes']
                
                #cleanup competitors tab
                competitors = {}
                for i in range(len(box_score['header']['competitions']['competitors'])):
                    competitors[str(i)] = box_score['header']['competitions']['competitors'][i]
                    #dropping unneeded columns in competitors-team tab
                    for column in ['logos', 'links']:
                        if column in competitors[str(i)]['team'].keys():
                            del competitors[str(i)]['team'][column]
                    #dropping unneeded columns in competitors tab
                    for column in ['linescores', 'record', 'probables']:
                        if column in competitors[str(i)].keys():
                            del competitors[str(i)][column]
                box_score['header']['competitions']['competitors'] = competitors

        return box_score
                
            
    def clean_stats(self, box_score):
        if 'boxscore' in box_score.keys():
            #==============================================================================================
            #removing athlete stats from box_score. make future functinoality to store these values as well
            #==============================================================================================
            if 'players' in box_score['boxscore'].keys():
                del box_score['boxscore']['players']
            teams = {}
            for i in range(len(box_score['boxscore']['teams'])):
                teams[str(i)] = box_score['boxscore']['teams'][i]
                if 'details' in teams[str(i)].keys():
                    del teams[str(i)]['details']
                if 'statistics' in teams[str(i)].keys():
                    stats = {}
                    for j in range(len(teams[str(i)]['statistics'])):
                        stats[str(j)] = teams[str(i)]['statistics'][j]
                        if 'stats' in stats[str(j)].keys():
                            stat_values = {}
                            for k in range(len(stats[str(j)]['stats'])):
                                stat_values[str(k)] = stats[str(j)]['stats'][k]
                            stats[str(j)]['stats'] = stat_values
                    teams[str(i)]['statistics'] = stats

            box_score['boxscore']['teams'] = teams
        return box_score


    def clean_boxscore(self, box_score):

        #deleting uneceassary items
        columns_to_delete = [
                            'notes', 'videos', 'news', 'playsMap', 'atBats', 'article', 'standings', 
                            'broadcasts', 'seasonseries', 'winprobability', 'againstTheSpread',
                            'predictor', 'odds', 'rosters'
                            ]
        for column in columns_to_delete:
            try:
                del box_score[column]
            except:
                pass

        #removing images array from venue dict
        try:
            del box_score['gameInfo']['venue']['images']
        except:
            pass
        #cleaning officials, plays, pickcenter tabs with helper functions
        box_score = self.clean_game_officials(box_score)
        box_score = self.transform_plays(box_score)
        box_score = self.clean_pickcenter(box_score)
        box_score = self.clean_header(box_score)
        box_score = self.clean_stats(box_score)

        return box_score



    def get_event_ids(self, date = None):
        '''
        Helper function to recieve all the event ids for a specific date. Returns 
        a list of event ids.
        '''
        try:
            scoreboard_data = ScoreBoardExtract(league = self.LEAGUE).get_scoreboard(date = date)['events']
        except:
            return None
        event_ids = []
        for i in range(len(scoreboard_data)):
            event_ids.append(scoreboard_data[i]['id'])
        
        if len(event_ids) > 0:
            return event_ids



    def save_boxscores(self, date = None, cluster = None, save_to_folder = False):
        '''
        Function to save the boxscore data for a specific game. Using the helper function 
        GET_BOXSCORE to retrive data and then utilizes the MongoDBClient class to store data.
        '''
        
        #if single event_id then turn it into a list to have loop work
        event_ids = self.get_event_ids(date = date)
        if event_ids:
            box_scores = []
            for i in range(len(event_ids)):
                box_score = self.get_boxscore(event_id = event_ids[i])
                box_scores.append(self.clean_boxscore(box_score))
                if not save_to_folder:
                    MongoDBClient(cluster=cluster).create_document(
                                                    db_name = self.LEAGUE,
                                                    collection_name = self.ENDPOINT,
                                                    document_id = event_ids[i],
                                                    content = box_scores[i]                                           
                                                )
                else:
                    wdir = 'data/raw/' + self.LEAGUE + '/' + self.ENDPOINT + '/'
                    try:
                        os.remove(wdir + event_ids[i] + '.json')
                        print(f'REMOVING FILE {event_ids[i]} TO REWRITE')
                    except:
                        pass
                    start_time = datetime.now()    
                    with open(wdir + event_ids[i] + '.json', 'w') as fp:
                        json.dump(box_scores[i], fp)
                    fp.close()
                    print(f'FILED {event_ids[i]} SAVED ... time to save: {datetime.now() - start_time} seconds')


        





if __name__ == '__main__':
    #BoxScoreExtract('mlb').save_boxscores(save_to_folder=True)
    print('finished')
