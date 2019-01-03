import unittest
import json
from application.routes.route import app

class TestApplication(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client()

    def test_home(self):
        res = self.tester.get('/')
        self.assertTrue(res.status_code == 200)
        self.assertTrue("Welcome to iReporter" in str(res.data))


    def test_create_red_flag(self):
        res = self.tester.post('/api/v1/red-flags', json={
            "createdOn": '14/10/2018',
            "createdBy": 1,
            "id":1,
            "incident_type": "red-flag",
            "location": "lat 0.00333 long 1.3456",
            "incident_status": "draft",
            "comment": "This is my comment."
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertTrue('Created red-flag record' in str(res.data))

    def test_getredflags(self):
        res = self.tester.get('/api/v1/red-flags')
        self.assertIn("data", str(res.data))
        self.assertEqual(res.status_code, 200)

    def test_getredflag(self):
        res = self.tester.get('/api/v1/red-flags/1')
        self.assertEqual(res.status_code, 200)

    def test_redflag_not_found(self):
        res = self.tester.get('/api/v1/red-flags/4')
        self.assertTrue(res.status_code == 404)
        self.assertTrue('Red-flag not available' in str(res.data))
