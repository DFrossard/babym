import os
from babym.environments import Environments
from pymongo import MongoClient

APP_ENV = os.environ.get('BABYM_ENV')
LOCALHOST_ADDRESS = 'localhost'
STAGING_ADDRESS = ''
PRODUCTION_ADDRESS = ''
TEST_ADDRESS = LOCALHOST_ADDRESS
DEFAULT_PORT = 27017

class BabymMongoClient():
    def __init__(self) -> None:
        if APP_ENV == Environments.development:
            self.client = MongoClient(LOCALHOST_ADDRESS, DEFAULT_PORT)
            self.baby_db = self.client['dev_baby_db']
        if APP_ENV == Environments.staging:
            self.client = MongoClient(STAGING_ADDRESS, DEFAULT_PORT)
            self.baby_db = self.client['staging_baby_db']
        if APP_ENV == Environments.production:
            self.client = MongoClient(PRODUCTION_ADDRESS, DEFAULT_PORT)
            self.baby_db = self.client['baby_db']
        if APP_ENV == Environments.test:
            self.client = MongoClient(TEST_ADDRESS, DEFAULT_PORT)
            self.baby_db = self.client['test_baby_db']
        
        self.babies_collection = self.baby_db['babies']
