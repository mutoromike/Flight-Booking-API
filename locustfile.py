import os
import json
from locust import HttpLocust, TaskSet, task, seq_task

class UserBehavior(TaskSet):

    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)
        self.access_token = ""
        self.headers = {'Content-Type': 'application/json'}

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.access_token = self.login()
        self.headers = {'Authorization': self.access_token,
            'Content-Type': 'application/json'
        }

    def login(self):
        name = os.getenv('ADMIN_EMAIL')
        passw = os.getenv('ADMIN_PASSWORD')
        data = {
            "email": name, 
            "password": passw
        }
        result = self.client.post("/api/v1/auth/login", headers=self.headers, data=json.dumps(data))

        return json.loads(result._content)['access_token']



    @task()
    def index(self):
        self.client.get(
            '/api/v1/flights/all')

    @seq_task(1)
    def post_reservation(self):
        data = {
            "tickets": 3,
            "flight_id": 1,
            "ticket_type": "economy"
        }
        self.client.post('/api/v1/booking',
                         headers=self.headers,
            data=json.dumps(data))


class ApiClient(HttpLocust):
    task_set = UserBehavior
    host = "http://127.0.0.1:8000/"
    min_wait = 1000
    max_wait = 5000