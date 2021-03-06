""" /tests/test_passports.py """

import json
from tests.base import BaseTestCase


class PassportTestCase(BaseTestCase):
    """Test case for the images blueprint."""

    def test_passport_upload_and_deletion(self):
        """Test if a user can successfully upload and delete passport"""
        # Get token
        access_token = self.get_token()
        res = self.client().post('/api/v1/image', headers=dict(Authorization=access_token),
        data=json.dumps(self.passport), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        result = json.loads(res.data.decode())
        self.assertIn('Passport has been uploaded ', result['message'])

        result1 = self.client().post('/api/v1/image', headers=dict(Authorization=access_token),
        data=json.dumps(self.passport), content_type='application/json')
        self.assertEqual(result1.status_code, 400)

        result2 = self.client().get('/api/v1/image', headers=dict(Authorization=access_token),
        content_type='application/json')
        self.assertEqual(result2.status_code, 200)

        res = self.client().delete('/api/v1/image', headers=dict(Authorization=access_token),
        content_type='application/json')
        self.assertEqual(res.status_code, 200)
        result = json.loads(res.data.decode())
        self.assertIn('Passport successfully deleted', result['message'])