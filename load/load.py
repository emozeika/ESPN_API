import psycopg2
import os
import sys


#loading config variables from parent directory
base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(base_dir)
import config

class PostgresClient:
    '''
    Client to send csv data to postgres database.
    '''
    HOSTNAME = config.POSTGRES_HOSTNAME
    USERNAME = config.POSTGRES_USERNAME
    PASSWORD = config.POSTGRES_PWD
    PORT = config.POSTGRES_PORT
    
    
    CONNECTION = None
    CURSOR = None

    def __init__(self, database):
        self.DATABASE = database
        self.CONNECTION = psycopg2.connect(
                                        host = self.HOSTNAME,
                                        dbname = self.DATABASE,
                                        user = self.USERNAME,
                                        password = self.PASSWORD,
                                        port = self.PORT
        )

    def close_connection(self):
        self.CONNECTION.close()












if __name__ == '__main__':
    pass