import os
import unittest

from volcengine.tls.TLSService import TLSService

class TestTLSService(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = os.environ["VOLCENGINE_ENDPOINT"]
        self.region = os.environ["VOLCENGINE_REGION"]
        self.access_key_id = os.environ["VOLCENGINE_ACCESS_KEY_ID"]
        self.access_key_secret = os.environ["VOLCENGINE_ACCESS_KEY_SECRET"]

    def test_tls_service(self):
        tls_client1 = TLSService(self.endpoint, self.access_key_id, self.access_key_secret, self.region)
        tls_client2 = TLSService(
            self.endpoint + "test",
            self.access_key_id + "test",
            self.access_key_secret + "test",
            self.region + "test"
        )

        self.assertNotEqual(tls_client1, tls_client2)
        self.assertEqual(self.region, tls_client1.get_region())
        self.assertEqual(self.region + "test", tls_client2.get_region())

    def test_check_scheme_and_endpoint(self):
        endpoint = "http://tls-cn-beijing.ivolces.com"
        tls_client = TLSService(endpoint, self.access_key_id, self.access_key_secret, self.region)
        server_info = tls_client.get_service_info()
        self.assertEqual("http", server_info.scheme)
        self.assertEqual("tls-cn-beijing.ivolces.com", server_info.host)

        endpoint = "https://tls-cn-beijing.ivolces.com"
        tls_client = TLSService(endpoint, self.access_key_id, self.access_key_secret, self.region)
        server_info = tls_client.get_service_info()
        self.assertEqual("https", server_info.scheme)
        self.assertEqual("tls-cn-beijing.ivolces.com", server_info.host)

        endpoint = "tls-cn-beijing.ivolces.com"
        tls_client = TLSService(endpoint, self.access_key_id, self.access_key_secret, self.region)
        server_info = tls_client.get_service_info()
        self.assertEqual("https", server_info.scheme)
        self.assertEqual(endpoint, server_info.host)

if __name__ == '__main__':
    unittest.main()
