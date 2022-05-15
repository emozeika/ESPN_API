import pandas as pd
from datetime import datetime
import json
import os
import sys

#loading custom objects
from scoreboardtransform import ScoreboardTransform

#loading config variables from parent directory
base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(base_dir)
import config



class BaseballStats:
    LEAGUE = 'mlb'
    RAW_DATA_PATH = 'data/raw/mlb/stats/'
    CURATED_DATA_PATH = 'data/curated/mlb/'
    TABLE_NAME = 'stats'


    def __init__(self):
        pass

    def load_file_names(self, file_path):
        files = os.listdir(file_path)
        
        return files