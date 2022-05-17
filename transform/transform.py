import pandas as pd
import json
import os



class Transform():

    def __init__(self):
        pass


    def load_file_names(self, file_path):
        files = os.listdir(file_path)
        
        return files

    
    def open_file(self, file_name):
        file = open(self.RAW_DATA_PATH + file_name)
        raw_data = json.load(file)
        file.close()

        return raw_data
            




    #TODO: function to update scoreboard table
    def inherit_test(self):

        print('inheritance worked')