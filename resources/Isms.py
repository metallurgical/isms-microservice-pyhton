from flask_restful import reqparse, request
from six.moves import html_parser
from flask import current_app as app
from flask.views import MethodView
import json, urllib, requests

class Isms(MethodView):

    # Post request send to ISMS API.
    def post(self):

        response = ''

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

        # Validate field before proceed.
        if isinstance(self.fieldValidation(args), dict):
            return self.fieldValidation(args)

        htmlParser = html_parser.HTMLParser()

        phoneNumber = args['phone']
        message = urllib.quote_plus(htmlParser.unescape(args['message']))
        username = urllib.quote_plus(htmlParser.unescape(args['username']))
        password = urllib.quote_plus(htmlParser.unescape(args['password']))

        phone = '';

        # Single phone number or just a string of phone number.
        if isinstance(phoneNumber, basestring):
            if phoneNumber[:1] != '6':
                phone = '6' + phone

        # List of phone number.
        else:
            for item in phoneNumber:
                phone += self.checkCountryCode(item) + ','

            phone = phone[:-1]

        url = app.config['ISMS_ENDPOINT'] + 'un=' + username + '&pwd=' + password + '&dstno=' + phone + '&msg=' + message + '&type=1&sendid=63666'

        try:
            response = requests.get(url)
            return self.parseResponse(response.text)

        except:
            raise Exception('Seems like the ISMS server is temporarily down.')

        return response


    # Check for phone number if user put 6 in front
    # otherwise put it in.
    def checkCountryCode(self, phoneNumber):
        if phoneNumber[:1] != '6':
            return '6' + phoneNumber

        return phoneNumber

    # Get response code from ISMS response.
    def parseResponse(self, responseText):
        text = responseText.split('=')
        code = text[0].strip()
        message = text[1].strip()

        # Hypen(-) symbol only exist on Error Response
        if '-' in code:
            code = code[1:]

        return {
            'status': 'success' if code == 2000 else 'failed',
            'code': code,
            'message': message
        }

    # Validate request to check for compulsary field.
    def fieldValidation(self, args):
        compulsaryField = ('phone', 'message', 'username', 'password')
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
