from flask_restful import request
from six.moves import html_parser
import urllib, requests
from Isms import Isms

class Message(Isms):

    # Post request send to ISMS API.
    def post(self):

        response = ''

        args = super(Message, self).identifyContentType(request)

        # Validate field before proceed.
        if isinstance(super(Message, self).fieldValidation(args), dict):
            return super(Message, self).fieldValidation(args)

        htmlParser = html_parser.HTMLParser()

        phoneNumber = args['phone']

        # Encode input.
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
                phone += super(Message, self).checkCountryCode(item) + ';'

            phone = phone[:-1]

        url = self.app.config['ISMS_SEND_ENDPOINT'] + 'un=' + username + '&pwd=' + password + '&dstno=' + phone + '&msg=' + message + '&type=1&sendid=63666'

        try:
            response = requests.get(url)
            return super(Message, self).parseResponse(response.text)

        except:
            raise Exception('Seems like the ISMS server is temporarily down.')

        return response