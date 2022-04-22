
import requests
import pandas as pd
from datetime import datetime
import config
import json
import os
from config import BASEURL, VERSIONURL

class Extract:
    '''
    This is an extraction to pull the data for the main endpoints into NOSQL files to be consumed into the transformation layer


    '''
    LEAGUE_MAPPING = {
        'ncaam' : 'basketball/mens-college-basketball',
        'nba' : 'basketball/nba',
        'mlb' : 'baseball/mlb'
    }
    ENDPOINTS = {
        'games' : 'scoreboard', 
        'stats' : 'summary', 
        'teams' : 'teams'
    }

    BASEURL = config.BASEURL + config.VERSIONURL + 'sports/'


    def __init__(self):
        pass
    

    def list_leagues(self):
        print('------- League Endpoints --------')
        for key in self.LEAGUE_MAPPING.keys():
            print(key)
    
    
    def list_endpoints(self):
        print('------- Data Endpoints --------')
        for key in self.ENDPOINTS.keys():
            print(key)


    def setup_league_url(self, league):
        '''
        Function to create the base URL for the league we are looking for.
        Uses league mapping dict in config.py to find the right slug mapping.
        
        Parameters:
        -----------------------------------------------------------
        league: str, the league to get scorecard data from

        Output:
        ------------------------------------------------------------
        url: str, base root url to scorecard without added filters
        '''
        try:
            self.LEAGUE_MAPPING[league]
        except KeyError:
            raise KeyError("Invalid league name {}. Use one of the following leagues {}".format(league, list(self.LEAGUE_MAPPING.keys())))


        url = self.BASEURL +  self.LEAGUE_MAPPING[league]
        return url


    def setup_endpoint(self, league, endpoint, filters = {}, limit = None):
        '''
        Takes the base url and adds sets up endpoint with filters

        Parameters:
        -----------------------------------------------------
        league: str, the league to get scorecard data from
        endpoint : str, the data endpoint for url 
        filters: dict, dictionary to add any filters to 
        limit: int, how many events you would like to return

        Output:
        -----------------------------------------------------
        url: str, full url to make request
        '''
        try:
            self.ENDPOINTS[endpoint]
        except KeyError:
            raise KeyError('Invalid endpoint {}. Possible endpoints are: {}'.format(endpoint, list(self.ENDPOINTS.keys())))

        endpoint_url = self.setup_league_url(league) + '/' + self.ENDPOINTS[endpoint]

        if filters:
            endpoint_url = endpoint_url + '?'
            for filter, value in filters.items():
                endpoint_url = endpoint_url  + filter + '=' + str(value) + '&'

        if limit:
            endpoint_url = endpoint_url + 'limit=' + str(limit)
            


        return endpoint_url


    def get_request(self, league, endpoint, filters = {}, limit = None):
        '''
        Function to make get request from url

        Parameters:
        -----------------------------------------------------
        league: str, the league to get scorecard data from
        endpoint : str, the data endpoint for url 
        filters: dict, dictionary to add any filters to 
        limit: int, how many events you would like to return

        Output:
        -------------------------------------------------------
        page: dict, json formatted get request
        '''
        url = self.setup_endpoint(league, endpoint, filters, limit)
        page = requests.get(url).json()
        

        return page