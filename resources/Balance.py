from flask_restful import request
from six.moves import html_parser
import urllib, requests
from Isms import Isms

class Balance(Isms):

    def post(self):

        response = ''

        args = super(Balance, self).identifyContentType(request)

        fields = ('username', 'password')

        # Validate field before proceed.
        if isinstance(super(Balance, self).fieldValidation(args, fields), dict):
            return super(Balance, self).fieldValidation(args, fields)

        htmlParser = html_parser.HTMLParser()
        # Encode input.
        username = urllib.quote_plus(htmlParser.unescape(args['username']))
        password = urllib.quote_plus(htmlParser.unescape(args['password']))

        url = self.app.config['ISMS_BALANCE_ENDPOINT'] + 'un=' + username + '&pwd=' + password

        try:
            response = requests.get(url)
            return super(Balance, self).parseResponse(response.text)

        except:
            raise Exception('Seems like the ISMS server is temporarily down.')

        return response