import psycopg2
import os
import sys


#loading config variables from parent directory
base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(base_dir)
import config





class PostgreSQLClient:
    '''
    Client to send csv data to postgres database.
    '''
    HOSTNAME = config.POSTGRES_HOSTNAME
    USERNAME = config.POSTGRES_USERNAME
    PASSWORD = config.POSTGRES_PWD
    PORT = config.POSTGRES_PORT
    DATABASE = config.POSTGRES_DATABASE
    


    def __init__(self, database = None):
        if database:
            self.DATABASE = database
        self.CONNECTION = psycopg2.connect(
                                        host = self.HOSTNAME,
                                        dbname = self.DATABASE,
                                        user = self.USERNAME,
                                        password = self.PASSWORD,
                                        port = self.PORT
        )
        self.CURSOR = self.CONNECTION.cursor()
        self.CONNECTION.autocommit = True


    def connect_to_new_database(self, db_name):
        self.DATABASE = db_name
        self.CONNECTION = psycopg2.connect(
                                        host = self.HOSTNAME,
                                        dbname = self.DATABASE,
                                        user = self.USERNAME,
                                        password = self.PASSWORD,
                                        port = self.PORT
        )
        self.CURSOR = self.CONNECTION.cursor()
        self.CONNECTION.autocommit = True
        print(f'NOW CONNECTED TO {db_name} DATABASE')


    def create_database(self, db_name):
        
        sql_drop_text = f'DROP DATABASE IF EXISTS {db_name}'
        sql_create_text = f'CREATE DATABASE {db_name}'
        
        self.CURSOR.execute(sql_drop_text)
        self.CURSOR.execute(sql_create_text)
        print(f'DATEBASE {db_name} HAS BEEN CREATED')
        self.connect_to_new_database(db_name)


    def delete_database(self, db_name):
        
        sql_drop_text = f'DROP DATABASE IF EXISTS {db_name}'
        self.CURSOR.execute(sql_drop_text)
        print(f'DATEBASE {db_name} HAS BEEN DELETED')


    def create_table(self, table_name):

        sql_drop_text = f'DROP TABLE IF EXISTS {table_name}'
        sql_create_text = f'CREATE TABLE {table_name} ()'        

        self.CURSOR.execute(sql_drop_text)
        self.CURSOR.execute(sql_create_text)
        print(f'TABLE {table_name} CREATED in {self.DATABASE} DATABASE')
    

    def delete_table(self, table_name):

        sql_drop_text = f'DROP TABLE IF EXISTS {table_name}'
        self.CURSOR.execute(sql_drop_text)
        print(f'TABLE {table_name} HAS BEEN DELETED FROM DATABASE {self.DATABASE}')


    def list_tables(self):
        sql_list_text = f"SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;"

        self.CURSOR.execute(sql_list_text)
        table_list = self.CURSOR.fetchall()
        for schema, table in table_list:
            print(schema + ' | ' + table)


    def add_columns_to_table(self, table_name, columns_dict):
        
        for col_name, col_type in columns_dict.items():
            sql_add_text = f'ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {col_name} {col_type}'
            self.CURSOR.execute(sql_add_text)
            print(f'ADDED COLUMN {col_name} TO TABLE {table_name} IN DATABASE {self.DATABASE}')


    def close(self):
        if self.CURSOR:
            self.CURSOR.close()
        if self.CONNECTION:
            self.CONNECTION.close()












if __name__ == '__main__':

    table_cols = config.batting_stats_dtypes
    for key, value in table_cols.items():
        table_cols[key] = config.dtype_mappings[value]


    pgclient  = PostgreSQLClient('mlb')
    pgclient.create_table('stats')
    pgclient.list_tables()
    #pgclient.add_columns_to_table('stats', table_cols)
    pgclient.close()
'''
    pgclient  = PostgreSQLClient()
    pgclient.create_database('mlb')
    pgclient.create_table('stats')
    pgclient.close()
'''