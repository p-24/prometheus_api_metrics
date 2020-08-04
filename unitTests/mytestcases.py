import unittest
from src import app as test_file

appObj = test_file.CustomCollector


class MyTestCases(unittest.TestCase):

    def test_url_extract_success(self):
        status, resp_time = appObj.url_extract(self, url="https://httpstat.us/200")
        self.assertEqual(status, 1)
        print("=== Test1 ===")
        print("Status = {}, ResponseTime = {}".format(status, resp_time))

    def test_url_extract_fail(self):
        status, resp_time = appObj.url_extract(self, url="https://httpstat.us/503")
        self.assertEqual(status, 0)
        print("=== Test2 ===")
        print("Status = {}, ResponseTime = {}".format(status, resp_time))

    def test_service_status(self):
        service_status = test_file.metrics().status_code
        print("=== Test3 ===")
        print("Service Status = " + str(service_status))

    def test_api_response(self):
        response = test_file.app.test_client().get('/metrics')
        self.assertEqual(response.status_code, 200)
        print("=== Test4 ===")
        print("Api Response :: ", response.status_code)


if __name__ == '__main__':
    unittest.main()
