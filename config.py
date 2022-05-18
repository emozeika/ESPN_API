#================================================================================
# URL BASE STRINGS FOR ESPN API
#================================================================================
COREURL = 'http://sports.core.api.espn.com/'
BASEURL = 'https://site.api.espn.com/apis/site/'
VERSIONURL = 'v2/'




#================================================================================
# POSTGRES CLIENT INFO
#================================================================================

POSTGRES_HOSTNAME = 'localhost'
POSTGRES_USERNAME = 'postgres'
POSTGRES_PWD = 'Emoz3832!'
POSTGRES_PORT = 5432


POSTGRES_MLB_DB = 'mlb'
POSTGRES_NBA_DB = 'nba'




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
batting_stats_dtypes = {
    'event_id' : 'Int64',
    'team_id' : 'Int64',
    'event_team_id' : 'string',
    'hitByPitch' : 'Int64', 
    'groundBalls' : 'Int64',
    'strikeouts' : 'Int64', 
    'RBIs' : 'Int64', 
    'hits' : 'Int64', 
    'stolenBases' : 'Int64', 
    'walks' : 'Int64', 
    'runs' : 'Int64', 
    'atBats' : 'Int64', 
    'sacFlies' : 'Int64', 
    'homeRuns' : 'Int64', 
    'runnersLeftOnBase' : 'Int64', 
    'triples' : 'Int64', 
    'doubles' : 'Int64', 
    'flyBalls' : 'Int64', 
    'caughtStealing' : 'Int64',
    'totalBases' : 'Int64', 
    'plateAppearances' : 'Int64', 
    'extraBaseHits' : 'Int64', 
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
    'event_id' : 'Int64',
    'team_id' : 'Int64',
    'event_team_id' : 'string',
    'save' : 'Int64', 
    'groundBalls' : 'Int64', 
    'strikeouts' : 'Int64', 
    'sacFlies' : 'Int64', 
    'hits' : 'Int64', 
    'earnedRuns' : 'Int64', 
    'battersHit' : 'Int64',
    'walks' : 'Int64', 
    'runs' : 'Int64', 
    'stolenBases' : 'Int64', 
    'caughtStealing' : 'Int64', 
    'homeRuns' : 'Int64', 
    'triples' : 'Int64', 
    'balks' : 'Int64', 
    'flyBalls' : 'Int64', 
    'battersFaced' : 'Int64', 
    'holds' : 'Int64', 
    'doubles' : 'Int64', 
    'wildPitches' : 'Int64', 
    'atBats' : 'Int64', 
    'opponentTotalBases' : 'Int64',
    'blownSaves' : 'Int64', 
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
    'event_id' : 'Int64',
    'team_id' : 'Int64',
    'event_team_id' : 'string',
    'doublePlays' : 'Int64', 
    'errors' : 'Int64', 
    'passedBalls' : 'Int64', 
    'assists' : 'Int64', 
    'outfieldAssists' : 'Int64', 
    'pickoffs' : 'Int64',
    'catcherCaughtStealing' : 'Int64', 
    'catcherStolenBasesAllowed' : 'Int64', 
    'fieldingPct' : 'float64', 
    'rangeFactor' : 'float64',
    'zoneRating' : 'float64', 
    'catcherCaughtStealingPct' : 'float64'
}