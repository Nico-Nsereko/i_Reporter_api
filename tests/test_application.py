from application import app
import unittest
import json


class TestApplication(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client()

    def test_home(self):
        res = self.tester.get('/')
        self.assertIn("Welcome to iReporter" , str(res.data))
        self.assertEqual(res.status_code,200)
        

    def test_getredflags(self):
        res = self.tester.get('/api/v1/red-flags')
        self.assertIn("data", str(res.data))
        self.assertEqual(res.status_code, 200)
        
    def test_getredflag(self):
        res = self.tester.get('/api/v1/red-flags/1')
        self.assertEqual(res.status_code, 200)


    def test_create_red_flag(self):
        res = self.tester.post('/api/v1/red-flags', json={ "createdOn": '14/10/2018',"createdBy": 1,"type": "red-flag",
        "location": "lat 0.00333 long 1.3456", "status": "draft", "comment": "This is my comment."
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertTrue('Created red-flag record' in str(res.data))

        res = self.tester.post('/api/v1/red-flags', json={ "createdOn": '14/10/2018',"createdBy": 1,"type": "red-flag",
        "location": "lat 0.00333 long 1.3456", "status": "draft", "comment": "This is my comment."
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue('Red-flag already exists' in str(res.data))

    def test_create_invalid_red_flag(self):
        res = self.tester.post('/api/v1/red-flags', json={
            "createdOn": '14/10/2018',
        })
        data = json.loads(res.data)
        self.assertTrue('Please add missing fields' in str(res.data))

        res = self.tester.post('/api/v1/red-flags', json={"createdOn": '14/10/2018',"createdBy": 1,"type": "abc",
            "location": "lat 0.00333 long 1.3456","status": "draft","comment": "This is my comment." })
        data = json.loads(res.data)
        self.assertTrue('Incident type should' in str(res.data))
 
        res = self.tester.post('/api/v1/red-flags', json={"createdOn": '14/10/2018', "createdBy": 1, "type": "red-flag",
            "location": "lat 0.00333 long 1.3456", "status": "drr", "comment": "This is my comment." })
        data = json.loads(res.data)
        self.assertTrue('Incident status should either be' in str(res.data))

        res = self.tester.post('/api/v1/red-flags', json={"createdOn": '14/10/2018', "createdBy": "string", "type": "red-flag",
            "location": "lat 0.00333 long 1.3456", "status": "draft", "comment": "This is my comment." })
        data = json.loads(res.data)
        self.assertTrue('createdBy should be of integer type' in str(res.data))

        res = self.tester.post('/api/v1/red-flags', json={"createdOn": '14-10-2018', "createdBy": 1, "type": "red-flag",
            "location": "lat 0.00333 long 1.3456", "status": "draft", "comment": "This is my comment." })
        data = json.loads(res.data)
        self.assertTrue('Date format should be' in str(res.data))

        res = self.tester.post('/api/v1/red-flags', json={"createdOn": '14/10/2018', "createdBy": 1, "type": "red-flag",
            "location": "", "status": "draft", "comment": "This is my comment." })
        data = json.loads(res.data)
        self.assertTrue('The location should be a string' in str(res.data))

        res = self.tester.post('/api/v1/red-flags', json={"createdOn": '14/10/2018', "createdBy": 1, "type": "red-flag",
            "location": "lat 0.00333 long 1.3456", "status": "draft", "comment": "This" })
        data = json.loads(res.data)
        self.assertTrue('The comment should be a string' in str(res.data))

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

    def test_remove_redflag(self):
        res = self.tester.delete('/api/v1/red-flags/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue('deleted' in str(res.data))

    def test_not_edited_comment(self):
        res = self.tester.patch('/api/v1/red-flags/1/comment', json={
            'comment': ''
        })
        self.assertTrue(res.status_code == 400)
        self.assertIn("The comment should be a", str(res.data))

        res = self.tester.patch('/api/v1/red-flags/4/comment', json={
            'comment': 'This is a new comment'
        })
        self.assertTrue(res.status_code == 404)
        self.assertTrue("Red-flag not available" in str(res.data))

    def test_not_edited_location(self):
        res = self.tester.patch('/api/v1/red-flags/4/location', json={
            'location': "lat 0.44 long 1.23444"
        })
        self.assertTrue(res.status_code == 404)
        self.assertIn("Red-flag not",str(res.data))

        res = self.tester.patch('/api/v1/red-flags/1/location', json={
            'location': ""
        })
        self.assertTrue(res.status_code == 400)
        self.assertIn("The location should be",str(res.data))

    def test_redflag_not_deleted(self):
        res = self.tester.delete('/api/v1/red-flags/2')
        self.assertEqual(res.status_code, 404)
        self.assertTrue('not available' in str(res.data))
