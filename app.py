from flask_restful import Resource, Api
from flask import Flask, Blueprint
from resources import Isms

app = Flask(__name__, instance_relative_config=True)
api = Api(app)

# Load default configuration file.
app.config.from_object('config')

# Load instance configuration file.
app.config.from_pyfile('config.py')

# Register route.
api.add_resource(Isms.Isms, '/send')

if __name__ == '__main__':
    app.run(debug=True)