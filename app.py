from datetime import datetime, date

from flask import Flask
from flask.json.provider import DefaultJSONProvider
from pymongo import MongoClient

class UpdatedJSONProvider(DefaultJSONProvider):
    def default(self, o):
        if isinstance(o, date) or isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

app = Flask(__name__)
app.json = UpdatedJSONProvider(app)


# Set up a connection to the MongoDB server
client = MongoClient('mongodb://localhost:27017/')

# Use the 'baby_db' database
db = client['baby_db']

# Use the 'babies' collection
babies_collection = db['babies']

from babym.controllers.baby_controller import baby_controller
app.register_blueprint(baby_controller)