from pymongo import MongoClient

class MongoDBClient:

    LOCAL_CLUSTER = 'mongodb://localhost:27017/'

    def __init__(self):
        '''Instantiates mongo db client with cluster'''
        self.client = MongoClient(self.LOCAL_CLUSTER)

    def list_databases(self):
        ''' Loops through your Mongo Client clusters and prints out all the database names in it'''
        for db in self.client.list_databases():
            print(db)


    #TODO: Create function to connect to a database
    #TODO: Create function to connect to a collection
    #TODO: Create function to write to a collection
    #TODO: Create function to pull data from collection





MongoDBClient().list_databases()


