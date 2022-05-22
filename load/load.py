import psycopg2
import os
import sys
import pandas as pd

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
        
        sql_drop_text = f'DROP DATABASE IF EXISTS {db_name};'
        sql_create_text = f'CREATE DATABASE {db_name};'
        
        self.CURSOR.execute(sql_drop_text)
        self.CURSOR.execute(sql_create_text)
        print(f'DATEBASE {db_name} HAS BEEN CREATED')
        self.connect_to_new_database(db_name)


    def delete_database(self, db_name):
        
        sql_drop_text = f'DROP DATABASE IF EXISTS {db_name};'
        self.CURSOR.execute(sql_drop_text)
        print(f'DATEBASE {db_name} HAS BEEN DELETED')


    def create_table(self, table_name):

        sql_drop_text = f'DROP TABLE IF EXISTS {table_name};'
        sql_create_text = f'CREATE TABLE {table_name} ();'        

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
        tables = []
        for schema, table in table_list:
            tables.append(table)
        return tables


    def add_columns_to_table(self, table_name, columns_dict):
        
        for col_name, col_type in columns_dict.items():
            sql_add_text = f'ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {col_name} {col_type};'
            self.CURSOR.execute(sql_add_text)
            print(f'ADDED COLUMN {col_name} TO TABLE {table_name} IN DATABASE {self.DATABASE}')


    def fix_null_values(self, string):
        string = string.replace('<NA>', '')
        return string


    def create_row_string(self, table_name, data_dict):

        sql_insert_text = f"INSERT INTO {table_name} ("
        for col in data_dict.keys():
            sql_insert_text = sql_insert_text + col + ', '
        #removing last comma
        sql_insert_text =  sql_insert_text[:-2] + ') VALUES ('

        for i in range(len(data_dict.keys())):
            sql_insert_text += '%s, '
        #removing last comma
        sql_insert_text = sql_insert_text[:-2]  + ');'

        sql_insert_text = self.fix_null_values(sql_insert_text)
        return sql_insert_text
    
    
    def get_id_list(self, table_name, id_field):
        sql_id_text = f"SELECT {id_field} FROM {table_name};"
        self.CURSOR.execute(sql_id_text)
        query = self.CURSOR.fetchall()
        ids = []
        for row in query:
            ids.append(row[0])
        return ids


    def update_row_string(self, table_name, data_dict, id_field, id_value):
        
        sql_update_text = f"UPDATE {table_name} SET ("

        for col in data_dict.keys():
            sql_update_text = sql_update_text + col + ', '
        #removing last comma
        sql_update_text =  sql_update_text[:-2] + ') = ('

        for i in range(len(data_dict.keys())):
            sql_update_text += '%s, '
        #removing last comma
        sql_update_text = sql_update_text[:-2]  + ')'

        sql_update_text += f' WHERE {id_field} = {id_value};'
        sql_update_text = self.fix_null_values(sql_update_text)
        return sql_update_text
    

    def insert_row_helper(self, table_name, data_dict, id_field):

        if data_dict[id_field] in self.get_id_list(table_name, id_field):
            sql_text = self.update_row_string(table_name, data_dict, id_field, data_dict[id_field])
        else:
            sql_text = self.create_row_string(table_name, data_dict)
        values = tuple(data_dict.values())
        
        self.CURSOR.execute(sql_text, values)


    def insert_data(self, table_name, data_dict, id_field):
        #if we feed it a pandas dataframe convert to dict 
        if type(data_dict) == pd.core.frame.DataFrame:
            data_dict = data_dict.to_dict('list')
            

        if type(data_dict[id_field]) == list:
            for i in range(len(data_dict[id_field])):
                row_dict = {}
                for key in data_dict.keys():
                    if type(data_dict[key][i]) == pd._libs.missing.NAType:
                        row_dict[key] = None
                    else:
                        row_dict[key] = data_dict[key][i]
                print(row_dict[id_field])
                self.insert_row_helper(table_name, row_dict, id_field)
        else:
            self.insert_row_helper(table_name, data_dict, id_field)


    def close(self):
        if self.CURSOR:
            self.CURSOR.close()
        if self.CONNECTION:
            self.CONNECTION.close()












if __name__ == '__main__':

    table_cols = {}
    for key, value in config.scoreboard_dtypes.items():
        table_cols[key] = config.dtype_mappings[value]

    df = pd.read_csv('data\curated\mlb\scoreboard.csv', dtype= config.scoreboard_dtypes)

    pgclient  = PostgreSQLClient('mlb')
    pgclient.create_table('scoreboard')
    pgclient.add_columns_to_table('scoreboard', table_cols)
    pgclient.insert_data('scoreboard', df, 'event_id')
