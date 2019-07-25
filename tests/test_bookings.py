"""
File to handle testing of flight reservations
"""

import json

from tests.base import BaseTestCase

class BookingsTestCase(BaseTestCase):
    """
        Class to handle testing of bookings
    """

    def test_successful_reservation(self):
        """
        Test successful booking 
        """
        access_token = self.get_admin_token() 

        result = self.client().post('/api/v1/flights', headers=dict(Authorization=access_token),
        data=json.dumps(self.flight), content_type='application/json' )

        result1 = self.client().post('/api/v1/booking', headers=dict(Authorization=access_token),
        data=json.dumps(self.booking), content_type='application/json' )
        self.assertEqual(result1.status_code, 201)

    def test_reservation_request(self):
        """
        Test unsuccessful booking
        """
        access_token = self.get_admin_token() 

        result = self.client().post('/api/v1/flights', headers=dict(Authorization=access_token),
        data=json.dumps(self.flight), content_type='application/json' )

        result1 = self.client().post('/api/v1/booking', headers=dict(Authorization=access_token),
        data=json.dumps(self.bad_booking), content_type='application/json' )
        self.assertEqual(result1.status_code, 400)

        result2 = self.client().post('/api/v1/booking', headers=dict(Authorization=access_token),
        data=json.dumps(self.bad_booking1), content_type='application/json' )
        self.assertEqual(result2.status_code, 400)

        result3 = self.client().post('/api/v1/booking', headers=dict(Authorization=access_token),
        data=json.dumps(self.bad_booking2), content_type='application/json' )
        self.assertEqual(result3.status_code, 400)

        result4 = self.client().post('/api/v1/booking', headers=dict(Authorization=access_token),
        data=json.dumps(self.bad_booking3), content_type='application/json' )
        self.assertEqual(result4.status_code, 400)

    def test_unsuccessful_reservation(self):
        """
        Test unsuccessful booking
        """
        access_token = self.get_admin_token() 
        
        """Book Flight"""
        result1 = self.client().post('/api/v1/booking', headers=dict(Authorization=access_token),
        data=json.dumps(self.booking), content_type='application/json' )
        self.assertEqual(result1.status_code, 400)

    def test_get_day_bookings(self):
        """
        Test get all bookings on a specific day 
        """
        access_token = self.get_admin_token() 

        result = self.client().post('/api/v1/flights', headers=dict(Authorization=access_token),
        data=json.dumps(self.flight), content_type='application/json' )
        results = json.loads(result.data.decode())

        result3 = self.client().get('/api/v1/booking/{}'.format(results['id']), headers=dict(Authorization=access_token),
        data=json.dumps(self.date), content_type='application/json' )
        self.assertEqual(result3.status_code, 404)

        result1 = self.client().post('/api/v1/booking', headers=dict(Authorization=access_token),
        data=json.dumps(self.booking), content_type='application/json' )
        self.assertEqual(result1.status_code, 201)

        result = self.client().get('/api/v1/booking/{}'.format(results['id']), headers=dict(Authorization=access_token),
        data=json.dumps(self.date), content_type='application/json' )
        self.assertEqual(result.status_code, 200)

    def test_error_in_get_day_bookings(self):
        """
        Test error in get all bookings on a specific day
        """
        access_token = self.get_admin_token() 

        result = self.client().post('/api/v1/flights', headers=dict(Authorization=access_token),
        data=json.dumps(self.flight), content_type='application/json' )

        result1 = self.client().post('/api/v1/booking', headers=dict(Authorization=access_token),
        data=json.dumps(self.booking), content_type='application/json' )
        self.assertEqual(result1.status_code, 201)

        result = self.client().get('/api/v1/booking/{}'.format(5), headers=dict(Authorization=access_token),
        data=json.dumps(self.date), content_type
        ='application/json' )
        self.assertEqual(result.status_code, 404)

    def test_unsuccessful_reservation_approval(self):
        """
        Test unsuccessful reservation approval
        """
        access_token = self.get_admin_token()
        result2 = self.client().put('/api/v1/approve/{}'.format(5),
        headers=dict(Authorization=access_token), content_type='application/json' )
        self.assertEqual(result2.status_code, 404)

    def test_error_reservation_approval(self):
        """
        Test error reservation approval
        """
        access_token = self.get_admin_token() 

        result = self.client().post('/api/v1/flights', headers=dict(Authorization=access_token),
        data=json.dumps(self.flight), content_type='application/json' )

        result1 = self.client().post('/api/v1/booking', headers=dict(Authorization=access_token),
        data=json.dumps(self.booking), content_type='application/json' )
        self.assertEqual(result1.status_code, 201)
        results = json.loads(result1.data.decode())

        result2 = self.client().put('/api/v1/approve/{}'.format(results['id']),
        headers=dict(Authorization=access_token), content_type='application/json' )
        self.assertEqual(result2.status_code, 200)


    def test_successful_reservation_status(self):
        """
        Test successful status check
        """
        access_token = self.get_admin_token()
        new_access_token = self.get_token()

        result = self.client().post('/api/v1/flights', headers=dict(Authorization=access_token),
        data=json.dumps(self.flight), content_type='application/json' )

        result1 = self.client().post('/api/v1/booking', headers=dict(Authorization=access_token),
        data=json.dumps(self.booking), content_type='application/json' )
        self.assertEqual(result1.status_code, 201)
        results = json.loads(result1.data.decode())

        result2 = self.client().get('/api/v1/status/{}'.format(results["id"]), headers=dict(Authorization=access_token),
        content_type='application/json' )
        self.assertEqual(result2.status_code, 200)

        result4 = self.client().put('/api/v1/approve/{}'.format(results['id']),
        headers=dict(Authorization=access_token), content_type='application/json' )
        self.assertEqual(result4.status_code, 200)

        result5 = self.client().get('/api/v1/status/{}'.format(results["id"]), headers=dict(Authorization=access_token),
        content_type='application/json' )
        self.assertEqual(result5.status_code, 200)

        result3 = self.client().post('/api/v1/booking', headers=dict(Authorization=new_access_token),
        data=json.dumps(self.booking), content_type='application/json' )
        self.assertEqual(result3.status_code, 201)
        req = json.loads(result3.data.decode())

        res = self.client().get('/api/v1/status/{}'.format(req["id"]), headers=dict(Authorization=access_token),
        content_type='application/json' )
        self.assertEqual(res.status_code, 401)

    def test_unavailable_reservation_status(self):
        """
        Test unsuccessful status check
        """
        access_token = self.get_admin_token() 

        result = self.client().post('/api/v1/flights', headers=dict(Authorization=access_token),
        data=json.dumps(self.flight), content_type='application/json' )

        result1 = self.client().post('/api/v1/booking', headers=dict(Authorization=access_token),
        data=json.dumps(self.booking), content_type='application/json' )
        self.assertEqual(result1.status_code, 201)

        result2 = self.client().get('/api/v1/status/{}'.format(233), headers=dict(Authorization=access_token),
        content_type='application/json' )
        self.assertEqual(result2.status_code, 404)

    def test_unauthorized_reservation_status(self):
        """
        Test unauthorized status check
        """
        access_token = self.get_admin_token()
        new_access_token = self.get_token

        result = self.client().post('/api/v1/flights', headers=dict(Authorization=access_token),
        data=json.dumps(self.flight), content_type='application/json' )

        result1 = self.client().post('/api/v1/booking', headers=dict(Authorization=access_token),
        data=json.dumps(self.booking), content_type='application/json' )
        self.assertEqual(result1.status_code, 201)
        results = json.loads(result1.data.decode())
        result2 = self.client().get('/api/v1/status/{}'.format(results["id"]), headers=dict(Authorization=new_access_token),
        content_type='application/json' )
        self.assertEqual(result2.status_code, 401)