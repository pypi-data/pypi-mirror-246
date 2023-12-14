import unittest
from openmeter_client import OpenMeterClient


class TestOpenMeterClient(unittest.TestCase):

    def setUp(self):
        self.demo_api_key = '969AC556-9185-48B2-97D2-D72341911067'
        self.client = OpenMeterClient(personal_access_token=self.demo_api_key)

    def test_get_meta_data(self):
        results_list = self.client.get_meta_data(page=0)
        result = len(results_list)
        expected_result =  10
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()