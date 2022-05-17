#URL structure variables for ESPN API
COREURL = 'http://sports.core.api.espn.com/'
BASEURL = 'https://site.api.espn.com/apis/site/'
VERSIONURL = 'v2/'


#Mongo DB local cluster
LOCAL_CLUSTER = "mongodb://localhost:27017/"


#================================================================================
# BASEBALL TABLE DATA TYPES CONFIGURATION IF LOADING FROM CSV
#================================================================================

#scoreboard
scoreboard_dtypes = {
    'event_id' : 'Int64',
    'event_date' : 'string',
    'home_team_id' : 'Int64',
    'away_team_id' : 'Int64',
    'event_site_name' : 'string',
    'neutral_site' : 'bool',
    'home_team_score' : 'Int64',
    'away_team_score' : 'Int64',
    'season_type_id' : 'Int64',
    'season_type_name' : 'string',
    'season_year' : 'Int64'
}

#stats/boxscore
stats_dtypes = {
    'event_id' : 'Int64'
}