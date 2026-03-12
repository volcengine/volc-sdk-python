import unittest

from requests import Response
from requests import exceptions as req_exc

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_exception import TLSException
from volcengine.tls.util import TLSUtil


class TestQualityFixes(unittest.TestCase):
    def test_tls_exception_missing_fields(self):
        resp = Response()
        resp.status_code = 400
        resp.headers = {}
        resp._content = b'{"foo": "bar"}'

        e = TLSException(resp)
        self.assertTrue(isinstance(e.error_code, str))
        self.assertTrue(isinstance(e.error_message, str))
        self.assertTrue(len(str(e)) > 0)

    def test_tls_exception_non_json(self):
        resp = Response()
        resp.status_code = 500
        resp.headers = {}
        resp._content = b'not-json'

        e = TLSException(resp)
        self.assertEqual(e.error_code, resp.text)
        self.assertEqual(e.error_message, resp.text)

    def test_tls_exception_non_dict_json(self):
        resp = Response()
        resp.status_code = 500
        resp.headers = {}
        resp._content = b'["a", "b"]'

        e = TLSException(resp)
        self.assertEqual(e.error_code, resp.text)
        self.assertEqual(e.error_message, resp.text)

    def test_tls_util_replace_white_space_character(self):
        self.assertIsNone(TLSUtil.replace_white_space_character(None))
        self.assertEqual(TLSUtil.replace_white_space_character("a\r\n\tb"), "a\\r\\n\\tb")

    def test_should_retry_exception(self):
        s = TLSService(endpoint="example.com", access_key_id="ak", access_key_secret="sk", region="cn-beijing")
        self.assertTrue(s._TLSService__should_retry_exception(req_exc.Timeout()))
        self.assertTrue(s._TLSService__should_retry_exception(req_exc.ConnectionError()))
        self.assertFalse(s._TLSService__should_retry_exception(ValueError("bad")))


if __name__ == "__main__":
    unittest.main()
