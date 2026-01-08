# coding=utf-8
"""Unit tests for CreateShipper request and TLSService integration (without real backend).

本文件仅关注 CreateShipper 请求体结构与 TLSService 调用参数，不依赖真实后端环境。
"""

import os
import unittest
from unittest.mock import Mock, patch

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import CreateShipperRequest
from volcengine.tls.tls_responses import CreateShipperResponse
from volcengine.tls.data import ContentInfo, JsonInfo, TosShipperInfo, KafkaShipperInfo


class TestCreateShipper(unittest.TestCase):
    """CreateShipper 相关单元测试。"""

    def setUp(self):
        # 使用本地默认配置构造 TLSService，避免依赖真实环境变量和后端
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

    def test_content_info_json_serialization(self):
        """测试 ContentInfo JSON 序列化结构与键名。"""
        json_info = JsonInfo(enable=True, keys=["field1", "field2"], escape=False)
        content_info = ContentInfo(format="json", json_info=json_info)

        json_data = content_info.json()
        self.assertEqual(json_data["Format"], "json")
        self.assertIn("JsonInfo", json_data)
        self.assertEqual(json_data["JsonInfo"]["Enable"], True)
        self.assertEqual(json_data["JsonInfo"]["Keys"], ["field1", "field2"])
        self.assertEqual(json_data["JsonInfo"]["Escape"], False)

    def test_tos_shipper_info_json_serialization(self):
        """测试 TosShipperInfo JSON 序列化结构与键名。"""
        tos_info = TosShipperInfo(
            bucket="test-bucket",
            prefix="logs/",
            max_size=100,
            compress="gzip",
            interval=600,
            partition_format="%Y/%m/%d",
        )

        json_data = tos_info.json()
        self.assertEqual(json_data["Bucket"], "test-bucket")
        self.assertEqual(json_data["Prefix"], "logs/")
        self.assertEqual(json_data["MaxSize"], 100)
        self.assertEqual(json_data["Compress"], "gzip")
        self.assertEqual(json_data["Interval"], 600)
        self.assertEqual(json_data["PartitionFormat"], "%Y/%m/%d")

    def test_kafka_shipper_info_json_serialization(self):
        """测试 KafkaShipperInfo JSON 序列化结构与键名。"""
        kafka_info = KafkaShipperInfo(
            instance="kafka-instance",
            kafka_topic="test-topic",
            compress="snappy",
            start_time=1234567890000,
            end_time=1234567899999,
        )

        json_data = kafka_info.json()
        self.assertEqual(json_data["Instance"], "kafka-instance")
        self.assertEqual(json_data["KafkaTopic"], "test-topic")
        self.assertEqual(json_data["Compress"], "snappy")
        self.assertEqual(json_data["StartTime"], 1234567890000)
        self.assertEqual(json_data["EndTime"], 1234567899999)

    def test_create_shipper_request_trn_and_time_fields(self):
        """测试 CreateShipperRequest 中 Trn 与时间字段的序列化。"""
        content_info = ContentInfo(
            format="json",
            json_info=JsonInfo(enable=True),
        )
        tos_shipper_info = TosShipperInfo(
            bucket="test-bucket",
            prefix="logs/",
            max_size=5,
            compress="snappy",
            interval=300,
            partition_format="%Y/%m/%d",
        )

        request = CreateShipperRequest(
            topic_id="test-topic-id",
            shipper_name="test-shipper",
            shipper_type="tos",
            content_info=content_info,
            tos_shipper_info=tos_shipper_info,
            shipper_start_time=1111111111111,
            shipper_end_time=2222222222222,
            role_trn="trn:iam::123456789012:role/test-role",
            service_trn="trn:iam::123456789012:role/service-role",
        )

        api_input = request.get_api_input()
        self.assertEqual(api_input["TopicId"], "test-topic-id")
        self.assertEqual(api_input["ShipperName"], "test-shipper")
        self.assertEqual(api_input["ShipperType"], "tos")
        self.assertEqual(api_input["RoleTrn"], "trn:iam::123456789012:role/test-role")
        self.assertEqual(
            api_input["ServiceTrn"], "trn:iam::123456789012:role/service-role"
        )
        self.assertEqual(api_input["ShipperStartTime"], 1111111111111)
        self.assertEqual(api_input["ShipperEndTime"], 2222222222222)

        # 嵌套结构
        self.assertIn("ContentInfo", api_input)
        self.assertIn("TosShipperInfo", api_input)
        self.assertEqual(api_input["TosShipperInfo"]["Bucket"], "test-bucket")

    @patch("volcengine.tls.TLSService.TLSService._TLSService__request")
    def test_create_shipper_service_call_tos(self, mock_request):
        """测试 TLSService.create_shipper 调用时的 API 名称与请求体结构。"""
        content_info = ContentInfo(
            format="json",
            json_info=JsonInfo(enable=True),
        )
        tos_shipper_info = TosShipperInfo(
            bucket="test-bucket",
            prefix="logs/",
            max_size=5,
            compress="snappy",
            interval=300,
            partition_format="%Y/%m/%d",
        )

        request = CreateShipperRequest(
            topic_id="test-topic-id",
            shipper_name="test-shipper",
            shipper_type="tos",
            content_info=content_info,
            tos_shipper_info=tos_shipper_info,
            role_trn="trn:iam::123456789012:role/test-role",
            service_trn="trn:iam::123456789012:role/service-role",
        )

        # 模拟 HTTP 响应
        mock_response = Mock()
        mock_response.headers = {
            "X-Tls-Requestid": "test-request-id",
            "Content-Type": "application/json",
        }
        mock_response.text = "{\"ShipperId\": \"shipper-123\"}"
        mock_request.return_value = mock_response

        response = self.tls_service.create_shipper(request)

        expected_body = request.get_api_input()
        mock_request.assert_called_once_with(api="/CreateShipper", body=expected_body)

        # 验证响应类型与 RequestId/字段解析
        self.assertIsInstance(response, CreateShipperResponse)
        self.assertEqual(response.get_shipper_id(), "shipper-123")
        self.assertEqual(response.get_request_id(), "test-request-id")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
