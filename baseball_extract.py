from boxscore import BoxScoreExtract
from datetime import datetime, timedelta

from scoreboard import ScoreBoardExtract

def pull_historical_data(league, start_date, end_date = None):
    '''
    Function to pull historical data based on dates. start_date and
    end_date should be in format YYYYMMDD
    '''
    #creating datetime values
    current_date = datetime.strptime(start_date, '%Y%m%d')
    if end_date:
        end_date = datetime.strptime(end_date, '%Y%m%d')
    else:
        end_date = datetime.today()

    #loop to run through dates
    while current_date < end_date:
        ScoreBoardExtract(league = league).save_scoreboard(date = current_date.strftime('%Y%m%d'), 
                                                            save_to_folder=True)
        BoxScoreExtract(league = league).save_boxscores(date = current_date.strftime('%Y%m%d'),
                                                            save_to_folder=True)

        current_date += timedelta(days = 1)

    
if __name__ == '__main__':
    pull_historical_data('mlb', '20120101')


