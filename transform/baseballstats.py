import pandas as pd
from datetime import datetime
import json
import os
import sys

#loading custom objects
from transform import Transform

#loading config variables from parent directory
base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(base_dir)
import config



class BaseballStats(Transform):
    LEAGUE = 'mlb'
    RAW_DATA_PATH = 'data/raw/mlb/stats/'
    CURATED_DATA_PATH = 'data/curated/mlb/'
    TABLE_NAME = 'stats'


    def __init__(self):
        super().__init__()


    def find_key(self, dict, value):
        for key in dict.keys():
            if value == dict[key]['name']:
                return key

    
    def get_stat_value(self, data, stat_name):
        if stat_name in data.keys():
            return data[stat_name]['value']
        else:
            return None
 

    def create_batting_table(self, file_name):
        '''
        This is a function to create the table for the stats for an event and save it to a csv.
        
        -------------------------------
        event_id (int) id from ESPN associated to the specific event
        team_id (int) id that regards to the current teams stats
        HBP (int) the amount times a batter was hit by pitch 
        GO (int) the amount of outs that came by ground balls
        SO (int) the amount of strikeouts in the game
        RBI (int)

        
        '''

        event_data = {
            'event_id' : [],
            'team_id' : []
        }

        raw_data = self.open_file(file_name)

        #adding event id to dict twice for each team row
        event_data['event_id'] = [raw_data['header']['id'] for i in range(2)]

        #abbrv of batting stat names 
        batting_stats = [
            'hitByPitch', 'groundBalls', 'strikeouts', 'RBIs', 'hits', 'stolenBases', 'walks', 
            'runs', 'atBats', 'sacFlies', 'homeRuns'
        ]

        #initalize empty list for each stat into dict
        for stat in batting_stats:
            event_data[stat] = []

        #grabbing stats for each team in statistics tab
        for key in raw_data['boxscore']['teams']:
            event_data['team_id'].append(raw_data['boxscore']['teams'][key]['team']['id'])
            batting_stats_key = self.find_key(raw_data['boxscore']['teams'][key]['statistics'], 'batting')
            
            for stat in batting_stats:
                if batting_stats_key is None:
                    event_data[stat].append(None)
                else:
                    stat_key = self.find_key(raw_data['boxscore']['teams'][key]['statistics'][batting_stats_key]['stats'], stat)
                    if stat_key is None:
                        event_data[stat].append(None)
                    else:
                        event_data[stat].append(raw_data['boxscore']['teams'][key]['statistics'][batting_stats_key]['stats'][stat_key]['value'])



        event_data = pd.DataFrame(event_data)
        print(event_data)








if __name__ == '__main__':
    BaseballStats().create_batting_table('401423754.json')