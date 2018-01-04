from flask_restful import reqparse, request
from six.moves import html_parser
from flask import current_app as app
from flask.views import MethodView
import json, urllib, requests

class Isms(MethodView):

    def __init__(self):
        self.app = app

    def identifyContentType(self, request):
        # If the request coming from normal form, then
        # parse individually using reqparse module.
        if request.content_type == 'application/x-www-form-urlencoded':
            parser = reqparse.RequestParser()
            parser.add_argument('phone', action='append', help="Phone field cannot be blank!")
            parser.add_argument('message', help="Message field cannot be blank!")
            parser.add_argument('username')
            parser.add_argument('password')
            args = parser.parse_args()

        # If the request is application/json?.
        else:
            args = request.get_json()

        return args

    # Check for phone number if user put 6 in front
    # otherwise put it in.
    def checkCountryCode(self, phoneNumber):
        if phoneNumber[:1] != '6':
            return '6' + phoneNumber

        return phoneNumber

    # Get response code from ISMS response.
    def parseResponse(self, responseText):
        # Only exist on send sms. Check balance are exceptional.
        if '=' in responseText:
            text = responseText.split('=')
            code = text[0].strip()
            message = text[1].strip()
        else:
            code = '2000'
            message = responseText

        # Hypen(-) symbol only exist on Error Response
        if '-' in code:
            code = code[1:]

        return {
            'status': 'success' if code == '2000' else 'failed',
            'code': code,
            'message': message
        }

    # Validate request to check for compulsary field.
    def fieldValidation(self, args, fields=None):
        compulsaryField = fields if fields is not None else ('phone', 'message', 'username', 'password')
        response = None

        for field in compulsaryField:
            # If key didnt exist, construct failed response.
            if field not in args:
                response = {'status': 'failed', 'message': 'Missing ' + field + ' parameter'}
                break

            # If key exist, but is empty, construct failed response.
            if args[field] is None:
                response = {'status': 'failed', 'message': 'Field ' + field + ' cannot be left empty'}
                break

        if response is not None:
            return response

        return True
