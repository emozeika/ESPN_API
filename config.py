#================================================================================
# URL BASE STRINGS FOR ESPN API
#================================================================================
COREURL = 'http://sports.core.api.espn.com/'
BASEURL = 'https://site.api.espn.com/apis/site/'
VERSIONURL = 'v2/'




#================================================================================
# POSTGRES CLIENT INFO AND MAPPINGS
#================================================================================

POSTGRES_HOSTNAME = 'localhost'
POSTGRES_USERNAME = 'postgres'
POSTGRES_PWD = 'Emoz3832!'
POSTGRES_PORT = 5432
POSTGRES_DATABASE = 'postgres'

POSTGRES_MLB_DB = 'mlb'
POSTGRES_NBA_DB = 'nba'

dtype_mappings = {
    'int64' : 'INT',
    'string' : 'VARCHAR(99)',
    'float64' : 'DOUBLE',
    'bool' : 'BOOL' 
}


#Mongo DB local cluster
LOCAL_CLUSTER = "mongodb://localhost:27017/"


#================================================================================
# BASEBALL TABLE DATA TYPES CONFIGURATION IF LOADING FROM CSV
#================================================================================

#scoreboard
scoreboard_dtypes = {
    'event_id' : 'int64',
    'event_date' : 'string',
    'home_team_id' : 'int64',
    'away_team_id' : 'int64',
    'home_team_name' : 'string',
    'away_team_name' : 'string',
    'event_site_name' : 'string',
    'neutral_site' : 'bool',
    'home_team_score' : 'int64',
    'away_team_score' : 'int64',
    'season_type_id' : 'int64',
    'season_type_name' : 'string',
    'season_year' : 'int64'
}

#stats/boxscore
batting_stats_dtypes = {
    'event_id' : 'int64',
    'team_id' : 'int64',
    'event_team_id' : 'string',
    'hitByPitch' : 'int64', 
    'groundBalls' : 'int64',
    'strikeouts' : 'int64', 
    'RBIs' : 'int64', 
    'hits' : 'int64', 
    'stolenBases' : 'int64', 
    'walks' : 'int64', 
    'runs' : 'int64', 
    'atBats' : 'int64', 
    'sacFlies' : 'int64', 
    'homeRuns' : 'int64', 
    'runnersLeftOnBase' : 'int64', 
    'triples' : 'int64', 
    'doubles' : 'int64', 
    'flyBalls' : 'int64', 
    'caughtStealing' : 'int64',
    'totalBases' : 'int64', 
    'plateAppearances' : 'int64', 
    'extraBaseHits' : 'int64', 
    'avg' : 'float64', 
    'slugAvg' : 'float64', 
    'onBasePct' : 'float64', 
    'OPS' : 'float64', 
    'atBatsPerHomeRun' : 'float64',
    'stolenBasePct' : 'float64', 
    'BIPA' : 'float64', 
    'offWARBR' : 'float64'
}

#stats/boxscore
pitching_stats_dtypes = {
    'event_id' : 'int64',
    'team_id' : 'int64',
    'event_team_id' : 'string',
    'save' : 'int64', 
    'groundBalls' : 'int64', 
    'strikeouts' : 'int64', 
    'sacFlies' : 'int64', 
    'hits' : 'int64', 
    'earnedRuns' : 'int64', 
    'battersHit' : 'int64',
    'walks' : 'int64', 
    'runs' : 'int64', 
    'stolenBases' : 'int64', 
    'caughtStealing' : 'int64', 
    'homeRuns' : 'int64', 
    'triples' : 'int64', 
    'balks' : 'int64', 
    'flyBalls' : 'int64', 
    'battersFaced' : 'int64', 
    'holds' : 'int64', 
    'doubles' : 'int64', 
    'wildPitches' : 'int64', 
    'atBats' : 'int64', 
    'opponentTotalBases' : 'int64',
    'blownSaves' : 'int64', 
    'ERA' : 'float64', 
    'WHIP' : 'float64', 
    'groundToFlyRatio' : 'float64', 
    'opponentAvg' : 'float64', 
    'opponentSlugAvg' : 'float64',
    'opponentOnBasePct' : 'float64', 
    'opponentOPS' : 'float64', 
    'strikeoutsPerNineInnings' : 'float64', 
    'strikeoutToWalkRatio' : 'float64', 
    'BIPA' : 'float64' 
}

#stats/boxscore
pitching_stats_dtypes = {
    'event_id' : 'int64',
    'team_id' : 'int64',
    'event_team_id' : 'string',
    'doublePlays' : 'int64', 
    'errors' : 'int64', 
    'passedBalls' : 'int64', 
    'assists' : 'int64', 
    'outfieldAssists' : 'int64', 
    'pickoffs' : 'int64',
    'catcherCaughtStealing' : 'int64', 
    'catcherStolenBasesAllowed' : 'int64', 
    'fieldingPct' : 'float64', 
    'rangeFactor' : 'float64',
    'zoneRating' : 'float64', 
    'catcherCaughtStealingPct' : 'float64'
}