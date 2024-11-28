import os
import unittest

from volcengine.tls.TLSService import TLSService

class TestTLSService(unittest.TestCase):

    def test_init(self):
        endpoint = os.environ["VOLCENGINE_ENDPOINT"]
        region = os.environ["VOLCENGINE_REGION"]
        access_key_id = os.environ["VOLCENGINE_ACCESS_KEY_ID"]
        access_key_secret = os.environ["VOLCENGINE_ACCESS_KEY_SECRET"]

        tls_client1 = TLSService(endpoint, access_key_id, access_key_secret, region)
        tls_client2 = TLSService(endpoint + "test", access_key_id + "test", access_key_secret + "test", region + "test")

        self.assertNotEqual(tls_client1, tls_client2)
        self.assertEqual(region, tls_client1.get_region())
        self.assertEqual(region + "test", tls_client2.get_region())

if __name__ == '__main__':
    unittest.main()