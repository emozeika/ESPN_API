from datetime import datetime
from pymongo import MongoClient
import config





class MongoDBClient:

    def __init__(self, cluster=None):
        '''Instantiates mongo db client with cluster'''
        if not cluster:
            self.CLUSTER = config.LOCAL_CLUSTER
        self.CLIENT = MongoClient(self.CLUSTER)

    def list_databases(self):
        ''' Loops through your Mongo Client clusters and prints out all the database names in it'''
        for db in self.CLIENT.list_databases():
            print(db)

    def create_database(self, df_name):
        self.CLIENT['db_name']


    def get_database(self, db_name):
        ''' Function to connect to a database'''
        self.DB = self.CLIENT.get_database(db_name)


    def list_collections(self, db_name):
        self.get_database(db_name)
        for coll in self.DB.list_collections():
            print(coll)
    
    #TODO: Create function to create a collection
    def create_collection(self, db_name, collection_name):
        '''Function to create a collection in a database'''
        self.CLIENT[db_name][collection_name]

    def close_connection(self):
        self.CLIENT.close()

    

    def check_document(self, db_name, collection_name, document_id):
        '''
        Runs through document ids in collection to determine if the document_id in question
        is in the collection already.
        '''
        raw_docs = list(self.CLIENT[db_name][collection_name].find())
        doc_ids = [raw_docs[i]['_id'] for i in range(len(raw_docs))]
        if document_id in doc_ids:
            return True
        else:
            return False
            



    def create_document(self, db_name, collection_name, document_id, content):

        start_time = datetime.now()
        if self.check_document(db_name, collection_name, document_id):
            print(f'REPLACING DOCUMENT IN [{db_name}-{collection_name}] WITH ID: {document_id}')
            self.CLIENT[db_name][collection_name].replace_one({'_id' : document_id}, {'data' : content})
            print(f"Took {datetime.now() - start_time} seconds to replace")
        else:
            print(f'SAVING DOCUMENT TO [{db_name}-{collection_name}] WITH ID: {document_id}')
            self.CLIENT[db_name][collection_name].insert_one({'_id': document_id, 'data' : content}, bypass_document_validation=True)
            print(f"Took {datetime.now() - start_time} seconds to save")



    def create_documents(self, db_name, collection_name, document_ids, contents):
        documents = []
        for i in range(len(document_ids)):
            #check if document is already in collection
            if self.check_document(db_name, collection_name, document_ids[i]):
                print(f'REPLACING DOCUMENT IN [{db_name}-{collection_name}] WITH ID: {document_ids[i]}')
                self.CLIENT[db_name][collection_name].replace_one({'_id' : document_ids[i]}, {'data' : contents[i]})
            else:
                documents.append({
                                    '_id' : document_ids[i],
                                    'data' : contents[i]
                                })
        #print(f'SAVING MULTIPLE DOCUMENTS TO [{db_name}-{collection_name}]')
        if len(documents) > 0:
            self.CLIENT[db_name][collection_name].insert_many(documents, bypass_document_validation=True)
        self.close_connection()




    #TODO: Create function to connect to a collection
    #TODO: Create function to pull data from collection





