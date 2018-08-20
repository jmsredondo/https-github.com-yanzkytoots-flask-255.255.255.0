import unittest
import requests


class BookTestCase(unittest.TestCase):
    def setUp(self):
        self.host = 'http://localhost:5000'
        self.sample_book = {'book_name': 'Noli Me Tangere', 'author': 'Jose Rizal',
                            'description': ' '}

    def test_book_add(self):
        """Test add a book"""
        result = requests.post(self.host + '/api/book', data=self.sample_book)
        self.assertEqual(result.status_code, 200)
        result = requests.get(self.host + '/api/book')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Noli Me Tangere', str(result.text))


class GenreTestCase(unittest.TestCase):
    def setUp(self):
        self.host = 'http://localhost:5000'
        self.sample_genre = {'genre': 'Tragedy', 'type': 'Fiction'}

    def test_genre_add(self):
        """Test add a genre"""
        result = requests.post(self.host + '/api/genre', data=self.sample_genre)
        self.assertEqual(result.status_code, 200)
        result = requests.get(self.host + '/api/genre')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Tragedy', str(result.text))


if __name__ == "__main__":
    unittest.main()
