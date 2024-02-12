"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app

# we need to import the file that contains the status codes
from src import status

class CounterTest(TestCase):
    """Counter tests"""

    def test_create_a_counter(self):
        """It should create a counter"""
        client = app.test_client()
        result = client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def setUp(self):
        self.client = app.test_client()

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        # Here we create a counter
        c_result = self.client.post('/counters/update_counter')
        self.assertEqual(c_result.status_code, status.HTTP_201_CREATED)

        # Here we get the counter
        b_result = self.client.get('/counters/update_counter')
        b_value = b_result.json['update_counter']

        u_result = self.client.put('/counters/update_counter')
        self.assertEqual(u_result.status_code, status.HTTP_200_OK)

        u_result = self.client.get('/counters/update_counter')
        u_value = u_result.json['update_counter']
        self.assertEqual(u_value, b_value + 1)

        # Check status code 404 with uncreated counter
        result = self.client.put('/counters/apple')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_a_counter(self):
        # Here we create a counter
        c_result = self.client.post('/counters/read_counter')
        self.assertEqual(c_result.status_code, status.HTTP_201_CREATED)

        # Here we read the counter
        result = self.client.get('/counters/read_counter')

        # Check status code 200
        self.assertEqual(result.status_code, status.HTTP_200_OK)

        # Assert that counter value is correct
        expected_value = 0
        actual_value = result.json['read_counter']
        self.assertEqual(actual_value, expected_value)

        # Check status code 404 with uncreated counter
        result = self.client.get('/counters/apple')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_a_counter(self):
        c_result = self.client.post('/counters/delete_counter')
        self.assertEqual(c_result.status_code, status.HTTP_201_CREATED)

        result = self.client.delete('/counters/delete_counter')

        self.assertEqual(result.status_code, status.HTTP_204_NO_CONTENT)

        result = self.client.get('/counters/delete_counter')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)
