import unittest
from main_api import app



class ApiTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

        try:
            self.assertEqual(app.debug, False)
        except Exception, e:
            print ('Debug mode is off: ', e)

    ######################################################################
    ############################ Login Test ##############################
    ######################################################################

    """Login Test"""

    def test_login_api(self):
        args = {}
        args['username'] = "testuser"
        args['password'] = "testpassword"

        response = self.call_login(args)
        print response

        self.assertEqual(response.status_code, 200)

    def call_login(self, params):
        return self.app.post('/users/login',
                             data=params,
                             follow_redirects = False
                             )


if __name__ == '__main__':
    unittest.main()
