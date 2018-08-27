import os
import unittest
import requests
<<<<<<< HEAD:tests/app_tests.py

from app import app
=======
from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False
app.config['DEBUG'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
>>>>>>> 7d58554477288213ff9701237f20c6795d6dfec3:test_cases.py


class BookTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.client = self.app.test_client()
        self.assertEqual(app.debug, False)
        self.host = 'http://localhost:5000'
        self.sample_book = {'book_name': 'Noli Me Tangere', 'author': 'Jose Rizal',
<<<<<<< HEAD:tests/app_tests.py
                            'description': ' ', 'image': ' '}

    def test01_test_book_add(self):
        """Test add a book"""
        requests.delete(self.host + '/book')
        rv = requests.post(self.host + '/book', data=self.sample_book)
        self.assertEqual(rv.status_code, 200)
        result = requests.get(self.host + '/book')
=======
                            'description': ' '}
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_book_add(self):
        """Test add a book"""
        result = requests.post(self.host + '/api/book', data=self.sample_book)
        self.assertEqual(result.status_code, 200)
        result = requests.get(self.host + '/api/book')
>>>>>>> 7d58554477288213ff9701237f20c6795d6dfec3:test_cases.py
        self.assertEqual(result.status_code, 200)
        self.assertIn('Noli Me Tangere', str(result.text))

    def test02_test_book_get_all(self):
        """Test get all books"""
        result = requests.get(self.host + '/book')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Noli Me Tangere', str(result.text))

    def test03_test_book_detail(self):
        """Test get a specific book"""
        result = requests.get(self.host + '/book/1')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Noli Me Tangere', str(result.text))

    def test04_test_book_update(self):
        """Test update a book"""
        rv = requests.put(
            self.host + '/book/1',
            data={'book_name': 'El Filibusterismo', 'author': 'Jose Rizal'}
        )
        self.assertEqual(rv.status_code, 200)
        result = requests.get(self.host + '/book/1')
        self.assertIn('El Filibusterismo', str(result.text))

    def test05_test_book_delete(self):
        """Test delete a book"""
        rv = requests.delete(self.host + '/book/1')
        self.assertEqual(rv.status_code, 200)
        result = requests.get(self.host + '/book/1')
        self.assertEqual(result.status_code, 404)


class GenreTestCase(unittest.TestCase):
    def setUp(self):
        self.host = 'http://localhost:5000'
        self.sample_genre = {'genre': 'Tragedy', 'type': 'Fiction'}
        requests.delete(self.host + '/genre')

    def test_genre_add(self):
        """Test add a genre"""
        result = requests.post(self.host + '/api/genre', data=self.sample_genre)
        self.assertEqual(result.status_code, 200)
        result = requests.get(self.host + '/api/genre')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Tragedy', str(result.text))


if __name__ == "__main__":
    unittest.main()
