import unittest
import app
import json

class SmsTestCase(unittest.TestCase):

   def setUp(self):
      self.app = app.app.test_client();
      app.testing = True

   '''
   Perform test using application/x-www-form-urlencoded.
   '''
   def test_can_send_form_encoded(self):
      response = self.app.post('/send', data=dict(
         phone=['60145127982'],
         message='hello from test 1',
         username=app.app.config['ISMS_USERNAME'],
         password=app.app.config['ISMS_PASSWORD']
      ))

      data = json.loads(response.get_data())

      self.assertEqual('2000', data.get('code'))

   '''
   Perform test using application/json.
   '''
   def test_can_send_application_json(self):
      response = self.app.post('/send', data=json.dumps(dict(
         phone=['60145127982'],
         message='hello from test 2',
         username=app.app.config['ISMS_USERNAME'],
         password=app.app.config['ISMS_PASSWORD']
      )), content_type='application/json')

      data = json.loads(response.get_data())

      self.assertEqual('2000', data.get('code'))

if __name__ == '__main__':
   unittest.main()