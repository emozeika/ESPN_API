from numpy import dtype
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
    BATTING_TABLE_NAME = 'batting'

    TABLE_MAPPING = {
        'batting' : 'batting_stats.csv',
        'pitching' : 'pitching_stats.csv'
    }

    DTYPE_MAPPING = {
        'batting' : config.batting_stats_dtypes
    }


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
        event_id (int)              id from ESPN associated to the specific event
        team_id (int)               id that regards to the current teams stats
        hitByPitch (int)            the amount times a batter was hit by pitch 
        groundBalls (int)           the amount of outs that came by ground balls
        strikeouts (int)            the amount of strikeouts in the game
        RBIs (int)                  number of runs batted in for the game
        hits (int)                  number of hits for the team in the game
        stolenBases (int)           number of stolen bases for the team in the game
        walks (int)                 number of base on balls in the game
        runs (int)                  number of runs scored for team in the game
        atBats (int)                number of at bats in the game
        sacFlies (int)              number of sacrifice flies for a team in the game
        homeRuns (int)              number of home runs for a team in the game
        runnersLeftOnBase (int)     number of home runs in the game
        triples (int)               number of triples for a team in the game
        doubles (int)               number of doubles for a team in the game
        flyBalls (int)              number of outs record by fly balls for a team in the game
        caughtStealing (int)        number of outs recorded by trying to steal in a game
        totalBases (int)            number of bases for a team in the game
        plateAppearances (int)      total number of at bats plus walks in the game for a team
        extraBaseHits (int)         number of hits not including singles in the game
        avg (float)                 batting average for team in the game
        slugAvg (float)             slugging percentage for team in the game
        onBasePct (float)           on base percentage for a team in the game
        OPS (float)                 on base percentage + slugging percentage for a team in the game
        atBatsPerHomeRun (float)    number of at bats for a home run for a team in the game
        stolenBasePct (float)       percentage of successful stolen base attempts in a game
        BIPA (float)                the batting average on balls put in play for a team in the game
        offWARBR (float)            offensive wins above replacement for team in the game
        '''

        event_data = {
            'event_id' : [],
            'team_id' : [],
            'event_team_id' : []
        }

        raw_data = self.open_file(file_name)

        #adding event id to dict twice for each team row
        event_data['event_id'] = [raw_data['header']['id'] for i in range(2)]

        #abbrv of batting stat names 
        batting_stats = [
            'hitByPitch', 'groundBalls', 'strikeouts', 'RBIs', 'hits', 'stolenBases', 'walks', 'runs', 'atBats', 
            'sacFlies', 'homeRuns', 'runnersLeftOnBase', 'triples', 'doubles', 'flyBalls', 'caughtStealing',
            'totalBases', 'plateAppearances', 'extraBaseHits', 'avg', 'slugAvg', 'onBasePct', 'OPS', 'atBatsPerHomeRun',
            'stolenBasePct', 'BIPA', 'offWARBR'
        ]

        #initalize empty list for each stat into dict
        for stat in batting_stats:
            event_data[stat] = []

        #grabbing stats for each team in statistics tab
        for key in raw_data['boxscore']['teams']:
            event_data['team_id'].append(raw_data['boxscore']['teams'][key]['team']['id'])
            event_data['event_team_id'].append(event_data['event_id'][0] + '~' + raw_data['boxscore']['teams'][key]['team']['id'])
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
        return event_data

    
    #TODO: create pitching stats table function
    def create_pitching_table(self, file_name):
        pass


    def concat_tables(self, table, new_table, id_field = None):
        if id_field:
            new_table = new_table[~new_table[id_field].isin(table[id_field])]

        table = pd.concat([table, new_table], axis = 0, ignore_index = True)
        return table

    
    def create_table(self, file_name, table_name):
        if table_name == 'batting':
            return self.create_batting_table(file_name)
        elif table_name == 'pitching':
            return self.create_pitching_table(file_name)


    def update_table(self, file_names, table_name, id_field = None):
        '''
        Table new should 
        '''
        if type(file_names) != list:
            file_names = [file_names]
    

        new_events = pd.DataFrame()

        for i in range(len(file_names)):
            if new_events.empty:
                new_events = self.create_table(file_names[i], table_name)
            else:
                new_events = self.concat_tables(new_events, self.create_table(file_names[i], table_name), id_field)

        #run logic to see if file is already created otherwise just save
        if self.TABLE_MAPPING[table_name] in os.listdir(base_dir + '/' + self.CURATED_DATA_PATH):
            stats_table = pd.read_csv(self.CURATED_DATA_PATH + self.TABLE_MAPPING[table_name])
            stats_table = self.concat_tables(stats_table, new_events, id_field)
            stats_table.to_csv(self.CURATED_DATA_PATH + self.TABLE_MAPPING[table_name], index = False)
        else:
            new_events.to_csv(self.CURATED_DATA_PATH + self.TABLE_MAPPING[table_name], index = False)

        




if __name__ == '__main__':
    BaseballStats().update_table(['401423754.json', '401431516.json', '320410111.json'], 'batting', 'event_team_id')