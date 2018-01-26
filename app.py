from flask_restful import Resource, Api
from resources.Message import Message
from resources.Balance import Balance
from flask import Flask, Blueprint

app = Flask(__name__, instance_relative_config=True)
api = Api(app)

# Load default configuration file.
app.config.from_object('config')

# Load instance configuration file.
app.config.from_pyfile('config.py')

# Register route.
api.add_resource(Message, '/sms/send')
api.add_resource(Balance, '/sms/check-balance')

if __name__ == '__main__':
    app.run() # use app.run(debug=True) for debugging