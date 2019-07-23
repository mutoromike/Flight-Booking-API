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
        """Create Flight"""
        result = self.client().post('/api/v1/flights', headers=dict(Authorization=access_token),
        data=json.dumps(self.flight), content_type='application/json' )
        """Book Flight"""
        result1 = self.client().post('/api/v1/booking', headers=dict(Authorization=access_token),
        data=json.dumps(self.booking), content_type='application/json' )
        self.assertEqual(result1.status_code, 201)

    def test_unsuccessful_reservation(self):
        """
        Test successful booking 
        """
        access_token = self.get_admin_token() 
        
        """Book Flight"""
        result1 = self.client().post('/api/v1/booking', headers=dict(Authorization=access_token),
        data=json.dumps(self.booking), content_type='application/json' )
        self.assertEqual(result1.status_code, 404)

    def test_get_day_bookings(self):
        """
        Test get all bookings on a specific day 
        """
        access_token = self.get_admin_token() 
        """Create Flight"""
        result = self.client().post('/api/v1/flights', headers=dict(Authorization=access_token),
        data=json.dumps(self.flight), content_type='application/json' )
        results = json.loads(result.data.decode())
        """Book Flight"""
        result1 = self.client().post('/api/v1/booking', headers=dict(Authorization=access_token),
        data=json.dumps(self.booking), content_type='application/json' )
        self.assertEqual(result1.status_code, 201)
        """Get all bookings"""
        result = self.client().get('/api/v1/booking/{}'.format(results['id']), headers=dict(Authorization=access_token),
        data=json.dumps(self.date), content_type='application/json' )
        self.assertEqual(result.status_code, 200)

    def test_successful_reservation_approval(self):
        """
        Test successful reservation approval
        """
        access_token = self.get_admin_token() 
        """Create Flight"""
        result = self.client().post('/api/v1/flights', headers=dict(Authorization=access_token),
        data=json.dumps(self.flight), content_type='application/json' )
        """Book Flight"""
        result1 = self.client().post('/api/v1/booking', headers=dict(Authorization=access_token),
        data=json.dumps(self.booking), content_type='application/json' )
        self.assertEqual(result1.status_code, 201)
        results = json.loads(result1.data.decode())
        """Approve flight"""
        result2 = self.client().put('/api/v1/approve/{}'.format(results['id']),
        headers=dict(Authorization=access_token), content_type='application/json' )
        self.assertEqual(result2.status_code, 200)

