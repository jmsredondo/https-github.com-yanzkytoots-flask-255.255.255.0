import unittest
import requests

from app import app


class BookTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.testing = True
        self.client = self.app.test_client
        self.assertEqual(app.debug, False)
        self.host = 'http://localhost:80'
        self.sample_book = {'book_name': 'Noli Me Tangere', 'author': 'Jose Rizal',
                            'description': ' ', 'image': ' '}

    def test01_test_book_add(self):
        """Test add a book"""
        requests.delete(self.host + '/book')
        rv = requests.post(self.host + '/book', data=self.sample_book)
        self.assertEqual(rv.status_code, 200)
        result = requests.get(self.host + '/book')
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
        self.host = 'http://localhost:80'
        self.sample_genre = {'genre': 'Tragedy', 'type': 'Fiction'}
        requests.delete(self.host + '/genre')

    def test_genre_add(self):
        """Test add a genre"""
        result = requests.post(self.host + '/genre', data=self.sample_genre)
        self.assertEqual(result.status_code, 200)
        result = requests.get(self.host + '/genre')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Tragedy', str(result.text))


if __name__ == "__main__":
    unittest.main()
