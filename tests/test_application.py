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

    def test_edit_location(self):
        res = self.tester.patch('/api/v1/red-flags/1/location', json=dict(
            location= "lat 0.44 long 1.23444"
        ))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("Updated red", str(res.data))
        self.assertIn("location", str(res.data))

    def test_edit_comment(self):
        res = self.tester.patch('/api/v1/red-flags/1/comment', json=(
            {
                'comment':'This is the updated comment'
            }
        ))
        data = json.loads(res.data)
        self.assertTrue(res.status_code == 200)
        self.assertIn("Updated red", str(res.data))
        self.assertIn("comment", str(res.data))

    def test_not_edited_comment(self):
        res = self.tester.patch('/api/v1/red-flags/1/comment', json={
            'comment': ''
        })
        self.assertTrue(res.status_code == 404)
        self.assertIn("Comment can", str(res.data))

        res = self.tester.patch('/api/v1/red-flags/4/comment', json={
            'comment': 'This is a new comment'
        })
        self.assertTrue(res.status_code == 400)
        self.assertTrue("Red-flag not available" in str(res.data))

    def test_not_edited_location(self):
        res = self.tester.patch('/api/v1/red-flags/4/location', json={
            'location': "lat 0.44 long 1.23444"
        })
        self.assertTrue(res.status_code == 400)
        self.assertIn("Red-flag not",str(res.data))

        res = self.tester.patch('/api/v1/red-flags/1/location', json={
            'location': ""
        })
        self.assertTrue(res.status_code == 404)
        self.assertIn("t be empty",str(res.data))

    def test_remove_redflag(self):
        res = self.tester.delete('/api/v1/red-flags/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue('deleted' in str(res.data))

    def test_redflag_not_deleted(self):
        res = self.tester.delete('/api/v1/red-flags/2')
        self.assertEqual(res.status_code, 400)
        self.assertTrue('not available' in str(res.data))
