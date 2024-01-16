import os
from datetime import datetime, date

from flask import Flask
from flask.json.provider import DefaultJSONProvider

from babym.controllers.baby_controller import baby_controller
from babym.controllers.parent_controller import parent_controller

class UpdatedJSONProvider(DefaultJSONProvider):
    def default(self, o):
        if isinstance(o, date) or isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

app = Flask(__name__)
app.json = UpdatedJSONProvider(app)

app.config['BABYM_ENV'] = os.environ.get('BABYM_ENV')

app.register_blueprint(baby_controller)
app.register_blueprint(parent_controller)