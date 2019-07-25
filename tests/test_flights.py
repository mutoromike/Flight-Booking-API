"""
File to handle testing of the created models
"""

import json

from tests.base import BaseTestCase

class FlightsTestCase(BaseTestCase):
    """
    This class represents the flights test case
    """


    def test_flight_creation(self):
        """
        Test if API can create a flight (POST request)
        """
        access_token = self.get_admin_token()

        result = self.client().post('/api/v1/flights', headers=dict(Authorization=access_token),
        data=json.dumps(self.flight), content_type='application/json' )
        self.assertEqual(result.status_code, 201)
        self.assertEqual(self.flight['name'], 'A596')

        result1 = self.client().post('/api/v1/flights', headers=dict(Authorization=access_token),
        data=json.dumps(self.flight), content_type='application/json' )
        self.assertEqual(result1.status_code, 302)

        result2 = self.client().post('/api/v1/flights', headers=dict(Authorization=access_token),
        data=json.dumps(self.flight1), content_type='application/json' )
        self.assertEqual(result2.status_code, 500)

    def test_empty_flight_fields(self):
        """
        Test empty flight fields.
        """
        access_token = self.get_admin_token()
        myflight = {'name': "", 'origin': "", 'destination': "", 'date': "",\
        'time': '10 pm'}
        res = self.client().post('/api/v1/flights', headers=dict(Authorization=access_token),
        data=json.dumps(myflight), content_type='application/json' )
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertIn('cannot be empty', result['message'])
        self.client().post('/api/v1/auth/logout', headers=dict(Authorization=access_token),
        content_type='application/json')
        resu = self.client().post('/api/v1/flights', headers=dict(Authorization=access_token),
        data=json.dumps(myflight), content_type='application/json' )
        self.assertEqual(resu.status_code, 401)

    def test_special_characters_in_flights_name(self):
        """
        Test special characters.
        """
        access_token = self.get_admin_token()
        myevent = {'name': "@# ha&(", 'origin': "Nairobi", 'destination': "Lagos", 'date': "12/12/2018",\
        'time': '12 pm'}
        res = self.client().post('/api/v1/flights', headers=dict(Authorization=access_token),
        data=json.dumps(myevent), content_type='application/json' )
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertIn('Flight name cannot have special', result['message'])

    def test_getting_all_flights(self):
        """
        Test API can get all Flights in the system (GET request).
        """
        access_token = self.get_token()
        # create a flight by making a POST request
        self.client().post(
            '/api/v1/flights',
            headers=dict(Authorization= access_token),
            data=json.dumps(self.flight), content_type='application/json')
        # get all the flights
        res = self.client().get(
            '/api/v1/flights/all')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.flight['name'], 'A596')

    def test_get_flight_by_id(self):
        """Test API can get a single flight by using it's id."""
        access_token = self.get_admin_token()
        # Create Flight
        req = self.client().post(
            '/api/v1/flights',
            headers=dict(Authorization= access_token),
            data=json.dumps(self.flight), content_type='application/json')
        # get the response data in json format
        results = json.loads(req.data.decode())

        result = self.client().get(
            '/api/v1/flight/{}'.format(results['id']),
            headers=dict(Authorization= access_token))
        # assert that the flight is actually returned given its ID
        self.assertEqual(result.status_code, 200)
        self.assertEqual(self.flight['name'], 'A596')

        result1 = self.client().get(
            '/api/v1/flight/{}'.format(23),
            headers=dict(Authorization= access_token))
        # assert that the error of the missing flight is returned
        self.assertEqual(result1.status_code, 404)

    def test_flight_editing(self):
        """Test API can edit an existing flight. (PUT request)"""
        access_token = self.get_admin_token()
        # Create a flight
        req = self.client().post(
            '/api/v1/flights',
            headers=dict(Authorization= access_token),
            data=json.dumps(self.flight), content_type='application/json')
        results = json.loads(req.data.decode())
        # Edit created flight data
        edit={"name": "A876", 'origin' : 'Sweden', 'destination' : 'Singapore',
                'date' : '12/1/2019', 'time' : '3 am'}
        req = self.client().put(
            '/api/v1/flight/{}'.format(results['id']),
            headers=dict(Authorization= access_token),
            data=json.dumps(edit), content_type='application/json')
        self.assertEqual(req.status_code, 200)

        # Get the edited flight
        results = self.client().get(
            '/api/v1/flight/{}'.format(results['id']),
            headers=dict(Authorization= access_token))
        self.assertIn("A876", str(results.data))

    def test_flights_created_by_admin(self):
        """Test API can edit an existing flight. (PUT request)"""
        access_token = self.get_admin_token()
        # Create a flight
        self.client().post(
            '/api/v1/flights',
            headers=dict(Authorization= access_token),
            data=json.dumps(self.flight), content_type='application/json')

        # Get the created flight
        results = self.client().get(
            '/api/v1/flights',
            headers=dict(Authorization= access_token))
        self.assertEqual(results.status_code, 200)
