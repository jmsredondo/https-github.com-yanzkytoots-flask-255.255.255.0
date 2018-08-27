import unittest
import requests
from flask import json

from tests import app, db


class BookTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.testing = True
        self.client = self.app.test_client
        self.assertEqual(app.debug, False)
        self.host = 'http://localhost:80'
        self.sample_book = {'book_name': 'Noli Me Tangere', 'author': 'Jose Rizal',
                            'description': ' ', 'image': ' '}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_book_add(self):
        """Test add a book"""
        result = requests.post(self.host + '/book', data=self.sample_book)
        self.assertEqual(result.status_code, 200)
        result = requests.get(self.host + '/book')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Noli Me Tangere', str(result.text))

    def test_book_get_all(self):
        """Test get all books"""
        result = self.client().post('/book/', data=self.sample_book)
        self.assertEqual(result.status_code, 200)
        result = self.client().get('/book/')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Noli Me Tangere', str(result.data))

    def test_book_detail(self):
        """Test get a specific book"""
        rv = self.client().post('/book/', data=self.sample_book)
        self.assertEqual(rv.status_code, 200)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/book/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Noli Me Tangere', str(result.data))

    def test_book_update(self):
        """Test update a book"""
        rv = self.client().post(
            '/book/',
            data={'book_name': 'El Filibusterismo', 'author': 'Jose Rizal'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/book/1',
            data={
                "book_name": "El Filibusterismo",
                "author": "Jose Rizal"
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/book/1')
        self.assertIn('El Filibusterismo', str(results.data))

    def test_book_delete(self):
        """Test delete a book"""
        rv = self.client().post(
            '/book/',
            data={'book_name': 'El Filibusterismo', 'author': 'Jose Rizal'})
        self.assertEqual(rv.status_code, 200)
        res = self.client().delete('/book/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/book/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


class GenreTestCase(unittest.TestCase):
    def setUp(self):
        self.host = 'http://localhost:80'
        self.sample_genre = {'genre': 'Tragedy', 'type': 'Fiction'}

    def test_genre_add(self):
        """Test add a genre"""
        result = requests.post(self.host + '/genre', data=self.sample_genre)
        self.assertEqual(result.status_code, 200)
        result = requests.get(self.host + '/genre')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Tragedy', str(result.text))


if __name__ == "__main__":
    unittest.main()
