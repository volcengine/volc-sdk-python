import unittest
from unittest.mock import patch

from volcengine.tls.TLSService import TLSService
from volcengine.tls.const import CONTENT_TYPE, APPLICATION_JSON, DESCRIBE_PROJECT, X_TLS_REQUEST_ID, X_SECURITY_TOKEN
from volcengine.tls.log_pb2 import LogGroupList
from volcengine.tls.producer.batch_semaphore import BatchSemaphore
from volcengine.tls.producer.log_dispatcher import LogDispatcher
from volcengine.tls.producer.producer import TLSProducer
from volcengine.tls.producer.producer_model import ProducerConfig
from volcengine.tls.producer.retry_queue import RetryQueue
from volcengine.tls.tls_exception import TLSException
from volcengine.tls.tls_requests import DeleteProjectRequest, PutLogsRequest, PutLogsV2Request, PutLogsV2Logs


ANONYMOUS_HEADER = "x-tls-anonymous-identity"


class _FakeResponse:
    status_code = 200
    text = ""
    content = b""
    headers = {
        CONTENT_TYPE: APPLICATION_JSON,
        X_TLS_REQUEST_ID: "request-id",
    }


class _CaptureSession:
    def __init__(self):
        self.requests = []

    def request(self, method, url, headers=None, data=None, timeout=None):
        self.requests.append({
            "method": method,
            "url": url,
            "headers": dict(headers or {}),
            "data": data,
            "timeout": timeout,
        })
        return _FakeResponse()


class _FailingSession:
    def request(self, *args, **kwargs):
        raise AssertionError("network request should not be sent")


def _make_put_logs_request():
    log_group_list = LogGroupList()
    log_group = log_group_list.log_groups.add()  # pylint: disable=no-member
    log = log_group.logs.add()
    log.time = 1
    content = log.contents.add()
    content.key = "k"
    content.value = "v"
    return PutLogsRequest("topic-id", log_group_list, compression=None)


def _make_put_logs_v2_request():
    logs = PutLogsV2Logs()
    logs.add_log({"k": "v"}, log_time=1)
    return PutLogsV2Request("topic-id", logs, compression=None)


class ApiKeyAnonymousAuthUnitTest(unittest.TestCase):
    def _service_with_api_key(self, api_key="api-key", access_key_id="", access_key_secret="", security_token=None):
        with patch("volcengine.base.Service.Service.init", lambda _self: None):
            if not hasattr(TLSService, "with_api_key"):
                self.fail("TLSService.with_api_key should exist")
            try:
                return TLSService.with_api_key(
                    "tls.example.com",
                    "cn-beijing",
                    api_key,
                    access_key_id=access_key_id,
                    access_key_secret=access_key_secret,
                    security_token=security_token,
                )
            except TypeError as e:
                self.fail("TLSService.with_api_key should accept optional AK/SK/token: {}".format(e))

    def _producer_config_with_api_key(self):
        try:
            return ProducerConfig("tls.example.com", "cn-beijing", "", "", api_key="api-key")
        except TypeError as e:
            self.fail("ProducerConfig.__init__ should accept api_key: {}".format(e))

    def test_with_api_key_put_logs_uses_anonymous_header_without_signature(self):
        service = self._service_with_api_key()
        service.session = _CaptureSession()

        with patch("volcengine.tls.TLSService.SignerV4.sign") as sign:
            service.put_logs(_make_put_logs_request())

        sign.assert_not_called()
        self.assertEqual(1, len(service.session.requests))
        headers = service.session.requests[0]["headers"]
        self.assertEqual("api-key", headers[ANONYMOUS_HEADER])
        self.assertNotIn("Authorization", headers)

    def test_reset_api_key_updates_anonymous_header(self):
        service = self._service_with_api_key("old-api-key")
        service.session = _CaptureSession()

        service.reset_api_key("new-api-key")
        with patch("volcengine.tls.TLSService.SignerV4.sign") as sign:
            service.put_logs(_make_put_logs_request())

        sign.assert_not_called()
        self.assertEqual("new-api-key", service.session.requests[0]["headers"][ANONYMOUS_HEADER])

    def test_put_logs_v2_uses_anonymous_header_without_signature(self):
        service = self._service_with_api_key()
        service.session = _CaptureSession()

        with patch("volcengine.tls.TLSService.SignerV4.sign") as sign:
            service.put_logs_v2(_make_put_logs_v2_request())

        sign.assert_not_called()
        self.assertEqual("api-key", service.session.requests[0]["headers"][ANONYMOUS_HEADER])
        self.assertNotIn("Authorization", service.session.requests[0]["headers"])

    def test_anonymous_put_logs_does_not_send_security_token(self):
        service = self._service_with_api_key(
            access_key_id="ak",
            access_key_secret="sk",
            security_token="sts-token",
        )
        service.session = _CaptureSession()

        with patch("volcengine.tls.TLSService.SignerV4.sign") as sign:
            service.put_logs(_make_put_logs_request())

        sign.assert_not_called()
        headers = service.session.requests[0]["headers"]
        self.assertEqual("api-key", headers[ANONYMOUS_HEADER])
        self.assertNotIn("Authorization", headers)
        self.assertNotIn(X_SECURITY_TOKEN, headers)

    def test_api_key_only_non_put_logs_fails_locally_without_network(self):
        service = self._service_with_api_key()
        service.session = _FailingSession()

        with self.assertRaises(TLSException) as ctx:
            service.delete_project(DeleteProjectRequest("project-id"))

        self.assertIn(ctx.exception.error_code, ("MissingCredentials", "InvalidCredentials"))
        self.assertIn("AK/SK", ctx.exception.error_message)

    def test_api_key_with_ak_sk_prefers_api_key_for_put_logs_and_signs_other_apis(self):
        service = self._service_with_api_key(access_key_id="ak", access_key_secret="sk")
        service.session = _CaptureSession()

        with patch("volcengine.tls.TLSService.SignerV4.sign") as sign:
            service.put_logs(_make_put_logs_request())

        sign.assert_not_called()
        headers = service.session.requests[0]["headers"]
        self.assertEqual("api-key", headers[ANONYMOUS_HEADER])
        self.assertNotIn("Authorization", headers)

        with patch("volcengine.tls.TLSService.SignerV4.sign") as sign:
            request = service._TLSService__prepare_request(api=DESCRIBE_PROJECT, params={"ProjectId": "project-id"})

        sign.assert_called_once()
        self.assertNotIn(ANONYMOUS_HEADER, request.headers)

    def test_producer_config_accepts_api_key_and_masks_it(self):
        config = self._producer_config_with_api_key()

        config.valid_config()

        self.assertEqual("api-key", config.client_config.api_key)
        self.assertNotIn("api-key", str(config))

    def test_log_dispatcher_passes_api_key_to_tls_service(self):
        config = self._producer_config_with_api_key()
        config.max_thread_count = 1
        captured = []

        class _FakeTLSService:
            def __init__(self, endpoint, access_key_id, access_key_secret, region,
                         security_token=None, scheme="https", timeout=60, api_version="0.3.0", api_key=None):
                captured.append({
                    "endpoint": endpoint,
                    "access_key_id": access_key_id,
                    "access_key_secret": access_key_secret,
                    "region": region,
                    "security_token": security_token,
                    "api_key": api_key,
                })

        with patch("volcengine.tls.producer.log_dispatcher.TLSService", _FakeTLSService):
            dispatcher = LogDispatcher(config, "producer", BatchSemaphore(1024), RetryQueue())
            dispatcher.close_now()

        self.assertEqual("api-key", captured[0]["api_key"])

    def test_log_dispatcher_reset_api_key_updates_tls_service(self):
        config = self._producer_config_with_api_key()
        reset_values = []

        class _FakeTLSService:
            def __init__(self, endpoint, access_key_id, access_key_secret, region,
                         security_token=None, scheme="https", timeout=60, api_version="0.3.0", api_key=None):
                self.api_key = api_key

            def reset_api_key(self, api_key):
                self.api_key = api_key
                reset_values.append(api_key)

        with patch("volcengine.tls.producer.log_dispatcher.TLSService", _FakeTLSService):
            dispatcher = LogDispatcher(config, "producer", BatchSemaphore(1024), RetryQueue())
            dispatcher.reset_api_key("new-api-key")
            dispatcher.close_now()

        self.assertEqual("new-api-key", config.client_config.api_key)
        self.assertEqual(["new-api-key"], reset_values)

    def test_producer_reset_api_key_updates_dispatcher_client(self):
        config = self._producer_config_with_api_key()
        reset_values = []

        class _FakeTLSService:
            def __init__(self, endpoint, access_key_id, access_key_secret, region,
                         security_token=None, scheme="https", timeout=60, api_version="0.3.0", api_key=None):
                self.api_key = api_key

            def reset_api_key(self, api_key):
                self.api_key = api_key
                reset_values.append(api_key)

        with patch("volcengine.tls.producer.log_dispatcher.TLSService", _FakeTLSService):
            producer = TLSProducer(config)
            producer.reset_api_key("new-api-key")
            producer.dispatcher.close_now()

        self.assertEqual("new-api-key", config.client_config.api_key)
        self.assertEqual(["new-api-key"], reset_values)


if __name__ == "__main__":
    unittest.main()
