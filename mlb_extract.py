from xarray import save_mfdataset
from extract import Extract
from mongoclient import MongoDBClient
from datetime import datetime

LEAGUE = 'mlb'
GAME_ENDPOINT = 'games'

def get_scoreboard(date = None):
    if not date:
        date = datetime.strftime(datetime.today(), "%Y%m%d")

    scoreboard = Extract().get_request(
                                        league = LEAGUE, 
                                        endpoint = GAME_ENDPOINT,
                                        filters = {'dates' : date}
                                    )

    return scoreboard
    
def save_scoreboard(date = None):
    if not date:
        date = datetime.strftime(datetime.today(), "%Y%m%d")

    scoreboard = get_scoreboard(date)
    MongoDBClient().create_document(
                                    db_name = LEAGUE, 
                                    collection_name = GAME_ENDPOINT, 
                                    document_id = date, 
                                    content = scoreboard
                                )


save_scoreboard()