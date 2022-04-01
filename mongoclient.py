from pymongo import MongoClient
import config

class MongoDBClient:

    def __init__(self, cluster=None):
        '''Instantiates mongo db client with cluster'''
        if not cluster:
            self.CLUSTER = config.LOCAL_CLUSTER
        self.client = MongoClient(self.CLUSTER)

    def list_databases(self):
        ''' Loops through your Mongo Client clusters and prints out all the database names in it'''
        for db in self.client.list_databases():
            print(db)


    #TODO: Create function to connect to a database
    #TODO: Create function to connect to a collection
    #TODO: Create function to write to a collection
    #TODO: Create function to pull data from collection





MongoDBClient().list_databases()


