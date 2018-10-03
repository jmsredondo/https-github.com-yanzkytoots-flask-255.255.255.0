import unitTest, requests, json


class TestCase(unitTest.TestCase):
    def setUp(self):
        self.host = 'http://localhost:9100'
        self.sample_book = \
            {
                'book_name': 'Noli Me Tangere',
                'author': 'Jose Rizal',
                'description': ' ',
                'image': ' '
            }
        self.sample_genre = \
            {
                'genre': 'Tragedy',
                'type': 'Fiction'
            }
        self.sample_user = \
            {
                'username': 'username',
                'firstName': 'Bob',
                'lastName': 'Stewart',
                'password': 'password',
                'email': 'bob_stewart@gmail.com',
                'phone': '64756000',
                'balance': 0
            }
        self.sample_login = \
            {
                'username': 'username',
                'password': 'password'
            }

    # CREATE RESOURCES #
    def test01_test_user_add(self):
        """Test add a user"""
        requests.delete(self.host + '/users')
        result = requests.post(self.host + '/users', data=self.sample_user)
        self.assertEqual(result.status_code, 200)
        result = requests.get(self.host + '/users')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Bob', str(result.text))

    def test02_test_user_login(self):
        result = requests.post(self.host + '/users/login', data=self.sample_login)
        self.assertEqual(result.status_code, 200)
        self.assertIn('username', str(result.text))

    def test03_test_book_add(self):
        """Test add a book"""
        result = requests.post(self.host + '/users/login', data=self.sample_login)
        temp = json.loads(result.content)
        token = temp['access_token']
        headers = {'Authorization': 'Bearer ' + token}
        requests.delete(self.host + '/book', headers=headers)
        rv = requests.post(self.host + '/book', data=self.sample_book, headers=headers)
        self.assertEqual(rv.status_code, 200)
        result = requests.get(self.host + '/book')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Noli Me Tangere', str(result.text))

    def test04_test_genre_add(self):
        """Test add a genre"""
        result = requests.post(self.host + '/users/login', data=self.sample_login)
        temp = json.loads(result.content)
        token = temp['access_token']
        headers = {'Authorization': 'Bearer ' + token}
        requests.delete(self.host + '/genre', headers=headers)
        result = requests.post(self.host + '/genre', data=self.sample_genre, headers=headers)
        self.assertEqual(result.status_code, 200)
        result = requests.get(self.host + '/genre')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Tragedy', str(result.text))

    # RETRIEVE RESOURCES #
    def test05_test_book_get_all(self):
        """Test get all books"""
        result = requests.get(self.host + '/book')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Noli Me Tangere', str(result.text))

    def test06_test_book_detail(self):
        """Test get a specific book"""
        result = requests.get(self.host + '/book/1')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Noli Me Tangere', str(result.text))

    def test06_test_user_get_all(self):
        """Test get all users"""
        result = requests.get(self.host + '/users')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Bob', str(result.text))

    def test07_test_user_detail(self):
        """Test get a specific user"""
        result = requests.get(self.host + '/users/1')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Bob', str(result.text))

    def test08_test_genre_get_all(self):
        """Test get all genres"""
        result = requests.get(self.host + '/genre')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Tragedy', str(result.text))

    def test09_test_genre_detail(self):
        """Test get a specific genre"""
        result = requests.get(self.host + '/genre/1')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Tragedy', str(result.text))

    # CATEGORY #
    def test10_test_add_book_to_genre(self):
        """Test add book to a genre"""
        result = requests.post(self.host + '/users/login', data=self.sample_login)
        temp = json.loads(result.content)
        token = temp['access_token']
        headers = {'Authorization': 'Bearer ' + token}
        rv = requests.post(
            self.host + '/genre/addbook/1',
            data={'book_id': '1'},
            headers=headers
        )
        self.assertEqual(rv.status_code, 200)
        result = requests.get(self.host + '/book/1')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Tragedy', str(result.text))

    def test11_test_get_genres_books(self):
        """Test get all books from a genre"""
        result = requests.get(self.host + '/genre/addbook/1')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Noli Me Tangere', str(result.text))

    # LIBRARY #
    def test12_test_add_book_to_library(self):
        """Test add book to a user library"""
        result = requests.post(self.host + '/users/login', data=self.sample_login)
        temp = json.loads(result.content)
        token = temp['access_token']
        headers = {'Authorization': 'Bearer ' + token}
        rv = requests.post(
            self.host + '/library',
            data=
            {
                'book_id': '1',
                'user_id': '1'
            },
            headers=headers
        )
        self.assertEqual(rv.status_code, 200)
        result = requests.get(self.host + '/library/1')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Noli Me Tangere', str(result.text))

    # def test013_test_get_books_from_library(self):
    #     """Test get all books from user library"""
    #     result = requests.get(self.host + '/library/1')
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn('Noli Me Tangere', str(result.text))

    # RATING #

    def test14_test_add_rating(self):
        """Test add rating to a book"""
        result = requests.post(self.host + '/users/login', data=self.sample_login)
        temp = json.loads(result.content)
        token = temp['access_token']
        headers = {'Authorization': 'Bearer ' + token}
        rv = requests.post(
            self.host + '/rate',
            data=
            {
                'book_id': '1',
                'user_id': '1',
                'rate': '1',
                'comment': 'Good book'
            },
            headers=headers
        )
        self.assertEqual(rv.status_code, 200)
        result = requests.get(self.host + '/rate/1')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Good book', str(result.text))

    def test15_test_get_book_rating(self):
        """Test get all books from user library"""
        result = requests.get(self.host + '/rate/1')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Good book', str(result.text))

    # UPDATE #
    def test16_test_book_update(self):
        """Test update a book"""
        result = requests.post(self.host + '/users/login', data=self.sample_login)
        temp = json.loads(result.content)
        token = temp['access_token']
        headers = {'Authorization': 'Bearer ' + token}
        rv = requests.put(
            self.host + '/book/1',
            data={'book_name': 'El Filibusterismo', 'author': 'Jose Rizal'},
            headers=headers
        )
        self.assertEqual(rv.status_code, 200)
        result = requests.get(self.host + '/book/1')
        self.assertIn('El Filibusterismo', str(result.text))

    def test17_test_user_update(self):
        """Test update a user"""
        result = requests.post(self.host + '/users/login', data=self.sample_login)
        temp = json.loads(result.content)
        token = temp['access_token']
        headers = {'Authorization': 'Bearer ' + token}
        rv = requests.put(
            self.host + '/users/1',
            data=
            {
                'username': 'username',
                'firstName': 'Howard',
                'lastName': 'Stewart',
                'password': 'password',
                'email': 'bob_stewart@gmail.com',
                'phone': '64756000',
                'balance': 0
            },
            headers=headers
        )
        self.assertEqual(rv.status_code, 200)
        result = requests.get(self.host + '/users/1')
        self.assertIn('Howard', str(result.text))

    def test18_test_genre_update(self):
        """Test update a book"""
        result = requests.post(self.host + '/users/login', data=self.sample_login)
        temp = json.loads(result.content)
        token = temp['access_token']
        headers = {'Authorization': 'Bearer ' + token}
        rv = requests.put(
            self.host + '/genre/1',
            data={'genre': 'Comedy', 'type': 'Fiction'},
            headers=headers
        )
        self.assertEqual(rv.status_code, 200)
        result = requests.get(self.host + '/genre/1')
        self.assertIn('Comedy', str(result.text))

    def test19_test_genre_delete(self):
        """Test delete a genre"""
        result = requests.post(self.host + '/users/login', data=self.sample_login)
        temp = json.loads(result.content)
        token = temp['access_token']
        headers = {'Authorization': 'Bearer ' + token}
        rv = requests.delete(self.host + '/genre/1', headers=headers)
        self.assertEqual(rv.status_code, 200)
        result = requests.get(self.host + '/genre/1')
        self.assertEqual(result.status_code, 404)

    def test20_test_book_delete(self):
        """Test delete a book"""
        result = requests.post(self.host + '/users/login', data=self.sample_login)
        temp = json.loads(result.content)
        token = temp['access_token']
        headers = {'Authorization': 'Bearer ' + token}
        rv = requests.delete(self.host + '/book/1', headers=headers)
        self.assertEqual(rv.status_code, 200)
        result = requests.get(self.host + '/book/1')
        self.assertEqual(result.status_code, 404)

    def test21_test_user_delete(self):
        """Test delete a user"""
        result = requests.post(self.host + '/users/login', data=self.sample_login)
        temp = json.loads(result.content)
        token = temp['access_token']
        headers = {'Authorization': 'Bearer ' + token}
        rv = requests.delete(self.host + '/users/1', headers=headers)
        self.assertEqual(rv.status_code, 200)
        result = requests.get(self.host + '/users/1')
        self.assertEqual(result.status_code, 404)


if __name__ == "__main__":
    unitTest.main()
