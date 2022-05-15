import json
import pandas as pd
import os
import sys
from datetime import datetime

#loading custom objects
from scoreboardtransform import ScoreboardTransform

#loading config variables from parent directory
base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(base_dir)
import config





class BaseballScoreboardTransform:
    LEAGUE = 'mlb'
    RAW_DATA_PATH = 'data/raw/mlb/games/'
    CURATED_DATA_PATH = 'data/curated/mlb/'
    TABLE_NAME = 'scoreboard'

    def __init__(self):
        pass

    def load_file_names(self, file_path):
        files = os.listdir(file_path)
        
        return files

    def create_events_for_date(self, file_name):
        '''
        Function to create the row of date for the event. This row will have the following
        fields

        -------------------------------
        event_date (date) in YYYYMMDD format
        event_id (int) id from ESPN associated to the specific event
        home_team_id (int) id for home team
        away_team_id (int) if for away team
        home_team_name (string) short name for home team    ie) Yankees, Red Sox, Rays
        away_team_name (string) short name for away team
        event_site_name (string) name where event is held
        neutral_site (bool) indicator if event was played on neutral site
        home_team_final (int) final score for home team
        away_team_final (int) final score for away team
        season_type_id (int) indicator of season type      ie) regular season, playoffs
        season_type_name (string) name of season type
        season_year (int) the year the season started in
        
        '''

        event_data = {
            'event_id' : [],
            'event_date' : [],
            'home_team_id' : [],
            'away_team_id' : [],
            'home_team_name' : [],
            'away_team_name' : [],
            'event_site_name' : [],
            'neutral_site' : [],
            'home_team_score' : [],
            'away_team_score' : [],
            'season_type_id' : [],
            'season_type_name' : [],
            'season_year' : []
        }   

        file = open(self.RAW_DATA_PATH + file_name)
        raw_data = json.load(file)
        file.close()

        if 'events' in raw_data.keys():
            for key in raw_data['events']:
                if raw_data['events'][key]['season']['type'] != 1:
                    #transform and append event_date
                    event_data['event_date'].append(raw_data['events'][key]['date'].split('T')[0].replace('-', ''))

                    #transform and append event_id
                    event_data['event_id'].append(int(raw_data['events'][key]['id']))

                    #logic to find home team key
                    if raw_data['events'][key]['competitions']['competitors']['0']['homeAway'] == 'home':
                        home_team_key, away_team_key = '0', '1'
                    else:
                        home_team_key, away_team_key = '1', '0'

                    #adding home/away teams id, name, score
                    event_data['home_team_id'].append(int(raw_data['events'][key]['competitions']['competitors'][home_team_key]['team']['id']))
                    event_data['away_team_id'].append(int(raw_data['events'][key]['competitions']['competitors'][away_team_key]['team']['id']))
                    event_data['home_team_name'].append(raw_data['events'][key]['competitions']['competitors'][home_team_key]['team']['name'])
                    event_data['away_team_name'].append(raw_data['events'][key]['competitions']['competitors'][away_team_key]['team']['name'])
                    event_data['home_team_score'].append(int(raw_data['events'][key]['competitions']['competitors'][home_team_key]['score']))
                    event_data['away_team_score'].append(int(raw_data['events'][key]['competitions']['competitors'][away_team_key]['score']))

                    #adding site name and neutral site indicator
                    if 'venue' in raw_data['events'][key]['competitions'].keys():
                        event_data['event_site_name'].append(raw_data['events'][key]['competitions']['venue']['fullName'])
                    else:
                        event_data['event_site_name'].append(None)
                    event_data['neutral_site'].append(raw_data['events'][key]['competitions']['neutralSite'])

                    #adding season type id and name
                    event_data['season_type_id'].append(int(raw_data['events'][key]['season']['type']))
                    event_data['season_type_name'].append(raw_data['events'][key]['season']['slug'])
                    event_data['season_year'].append(int(raw_data['events'][key]['season']['year']))
        
        event_table = pd.DataFrame(event_data)
        print(f"TABLE CREATED FOR {file_name.split('.')[0]}")
        return event_table



    def create_table(self, file_name):
        file_table = self.create_events_for_date(file_name)
        
        file_list = [string.split('.')[0] for string in os.listdir(base_dir + '/' + self.CURATED_DATA_PATH)]       
        if self.TABLE_NAME in file_list:
            #TODO: add logic to load in file if found then append to file
            scoreboard = pd.read_csv(self.CURATED_DATA_PATH + self.TABLE_NAME + '.csv', dtype = config.scoreboard_dtypes)
            file_table = file_table[~file_table['event_id'].isin(scoreboard['event_id'])]
            
            scoreboard = pd.concat([scoreboard, file_table], axis = 0, ignore_index = True)
            scoreboard.to_csv(self.CURATED_DATA_PATH + self.TABLE_NAME + '.csv', index = False)
        else:
            file_table.to_csv(self.CURATED_DATA_PATH + self.TABLE_NAME + '.csv', index = False)
        
    



    def save_new_events(self, file_list):
        if type(file_list) != list:
            file_list = [file_list]
        
        events_table = pd.DataFrame()

        for i in range(len(file_list)):
            if events_table.empty:
                events_table = self.create_events_for_date(file_list[i])
            else:
                new_events_table = self.create_events_for_date(file_list[i])
                new_events_table = new_events_table[~new_events_table['event_id'].isin(events_table['event_id'])]
                events_table = pd.concat([events_table, new_events_table], axis = 0, ignore_index = True)
        
        #saving new events to csv if one exists, otherwise saving table to csv
        curated_files = [string.split('.')[0] for string in os.listdir(base_dir + '/' + self.CURATED_DATA_PATH)]       
        if self.TABLE_NAME in curated_files:
            #TODO: add logic to load in file if found then append to file
            scoreboard = pd.read_csv(self.CURATED_DATA_PATH + self.TABLE_NAME + '.csv', dtype = config.scoreboard_dtypes)
            events_table = events_table[~events_table['event_id'].isin(scoreboard['event_id'])]
            
            #saving csv
            scoreboard = pd.concat([scoreboard, events_table], axis = 0, ignore_index = True)
            print('SAVING SCOREBOARD TABLE')
            scoreboard.to_csv(self.CURATED_DATA_PATH + self.TABLE_NAME + '.csv', index = False)
        else:
            print('SAVING SCOREBOARD TABLE')
            events_table.to_csv(self.CURATED_DATA_PATH + self.TABLE_NAME + '.csv', index = False)

















###################################################################################

if __name__ == '__main__' :
    file_list = os.listdir(base_dir + '/' 'data/raw/mlb/games')
    BaseballScoreboardTransform().save_new_events(file_list)