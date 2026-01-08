"""TLSService.describe_shipper 的请求构造与异常场景单元测试（无需真实后端）。"""

import os
import unittest
from unittest.mock import patch, Mock

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import DescribeShipperRequest
from volcengine.tls.tls_exception import TLSException


class TestDescribeShipper(unittest.TestCase):
    """测试 DescribeShipper 请求结构与 TLSService 调用行为。"""

    def setUp(self):
        self.endpoint = os.environ.get(
            "VOLCENGINE_ENDPOINT", "https://tls-cn-beijing.ivolces.com"
        )
        self.region = os.environ.get("VOLCENGINE_REGION", "cn-beijing")
        self.access_key_id = os.environ.get("VOLCENGINE_ACCESS_KEY_ID", "test-ak")
        self.access_key_secret = os.environ.get(
            "VOLCENGINE_ACCESS_KEY_SECRET", "test-sk"
        )

        self.tls_service = TLSService(
            self.endpoint,
            self.access_key_id,
            self.access_key_secret,
            self.region,
        )

    def test_describe_shipper_request_body(self):
        """验证 DescribeShipperRequest.get_api_input 顶层键名。"""
        request = DescribeShipperRequest(shipper_id="shipper-123")
        api_input = request.get_api_input()

        self.assertEqual(api_input["ShipperId"], "shipper-123")

    @patch("volcengine.tls.TLSService.TLSService._TLSService__request")
    def test_describe_shipper_nonexistent_shipper(self, mock_request):
        """模拟投递配置不存在时，TLSService.describe_shipper 抛出异常并携带正确请求参数。"""
        shipper_id = "nonexistent-shipper-id"
        request = DescribeShipperRequest(shipper_id=shipper_id)

        # 配置底层 __request 抛出 TLSException，模拟后端 404/NotFound 场景
        mock_request.side_effect = TLSException(
            error_code="NotFound", error_message="Shipper not found"
        )

        with self.assertRaises(TLSException):
            self.tls_service.describe_shipper(request)

        # 验证 __request 调用参数
        mock_request.assert_called_once()
        _, kwargs = mock_request.call_args
        self.assertEqual(kwargs.get("api"), "/DescribeShipper")
        params = kwargs.get("params")
        self.assertIsInstance(params, dict)
        self.assertEqual(params.get("ShipperId"), shipper_id)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
