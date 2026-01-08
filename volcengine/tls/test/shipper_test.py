# coding: utf-8
"""Unit tests for TLS Shipper functionality (DeleteShipper / ModifyShipper).

本文件仅关注请求体结构与 TLSService 调用参数，不依赖真实后端环境。
"""

import os
import unittest
from unittest.mock import Mock, patch

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import (
    DeleteShipperRequest,
    ModifyShipperRequest,
)
from volcengine.tls.tls_responses import DeleteShipperResponse, ModifyShipperResponse
from volcengine.tls.data import ContentInfo, JsonInfo, TosShipperInfo, KafkaShipperInfo, CsvInfo


class TestDeleteShipper(unittest.TestCase):
    """DeleteShipper 相关单元测试。"""

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

    def test_delete_shipper_request_validation(self):
        """测试 DeleteShipperRequest.check_validation 仅校验非 None。"""
        # 合法 shipper_id
        valid_request = DeleteShipperRequest(shipper_id="test-shipper-123")
        self.assertTrue(valid_request.check_validation())

        # shipper_id 为 None 判定为非法
        invalid_request = DeleteShipperRequest(shipper_id=None)
        self.assertFalse(invalid_request.check_validation())

    def test_delete_shipper_request_api_input(self):
        """测试 DeleteShipperRequest.get_api_input 顶层键名。"""
        shipper_id = "test-shipper-456"
        request = DeleteShipperRequest(shipper_id=shipper_id)
        api_input = request.get_api_input()

        # 应将 shipper_id 转换为 ShipperId
        self.assertIn("ShipperId", api_input)
        self.assertEqual(api_input["ShipperId"], shipper_id)

    @patch("volcengine.tls.TLSService.TLSService._TLSService__request")
    def test_delete_shipper_service_call(self, mock_request):
        """测试 TLSService.delete_shipper 调用的 API 名称与请求体结构。"""
        mock_response = Mock()
        mock_response.headers = {
            "X-Tls-Requestid": "test-request-id",
            "Content-Type": "application/json",
        }
        mock_response.text = "{}"
        mock_request.return_value = mock_response

        request = DeleteShipperRequest(shipper_id="shipper-123")
        response = self.tls_service.delete_shipper(request)

        mock_request.assert_called_once_with(
            api="/DeleteShipper", body={"ShipperId": "shipper-123"}
        )
        self.assertIsInstance(response, DeleteShipperResponse)
        self.assertEqual(response.get_request_id(), "test-request-id")


class TestModifyShipper(unittest.TestCase):
    """ModifyShipper 相关单元测试。"""

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

    def test_modify_shipper_validation(self):
        """测试 ModifyShipperRequest.check_validation 仅校验 ShipperId 非空。"""
        invalid_request = ModifyShipperRequest(
            shipper_id=None,
            shipper_name="test-shipper",
        )
        self.assertFalse(invalid_request.check_validation())

        valid_request = ModifyShipperRequest(shipper_id="test-shipper-id")
        self.assertTrue(valid_request.check_validation())

    def test_modify_shipper_api_input_tos_with_trn_and_time(self):
        """测试 ModifyShipperRequest TOS 配置下的请求体结构、Trn 与时间字段。"""
        content_info = ContentInfo(
            format="json",
            json_info=JsonInfo(enable=True, keys=["field1", "field2"], escape=False),
        )

        tos_shipper_info = TosShipperInfo(
            prefix="test-prefix",
            max_size=10,
            compress="gzip",
            interval=600,
            partition_format="%Y/%m/%d",
        )

        modify_shipper_request = ModifyShipperRequest(
            shipper_id="test-shipper-id",
            shipper_name="test-shipper-name",
            shipper_type="tos",
            status=True,
            content_info=content_info,
            tos_shipper_info=tos_shipper_info,
            shipper_start_time=1111111111111,
            shipper_end_time=2222222222222,
            role_trn="trn:iam::123456789012:role/test-role",
            service_trn="trn:iam::123456789012:role/service-role",
        )

        api_input = modify_shipper_request.get_api_input()

        # 顶层字段
        self.assertEqual(api_input["ShipperId"], "test-shipper-id")
        self.assertEqual(api_input["ShipperName"], "test-shipper-name")
        self.assertEqual(api_input["ShipperType"], "tos")
        self.assertEqual(api_input["Status"], True)
        self.assertEqual(api_input["RoleTrn"], "trn:iam::123456789012:role/test-role")
        self.assertEqual(
            api_input["ServiceTrn"], "trn:iam::123456789012:role/service-role"
        )
        self.assertEqual(api_input["ShipperStartTime"], 1111111111111)
        self.assertEqual(api_input["ShipperEndTime"], 2222222222222)

        # ContentInfo 嵌套结构
        self.assertIn("ContentInfo", api_input)
        content_info_data = api_input["ContentInfo"]
        self.assertEqual(content_info_data["Format"], "json")
        self.assertIn("JsonInfo", content_info_data)
        json_info_data = content_info_data["JsonInfo"]
        self.assertEqual(json_info_data["Enable"], True)
        self.assertEqual(json_info_data["Keys"], ["field1", "field2"])
        self.assertEqual(json_info_data["Escape"], False)

        # TOS ShipperInfo 嵌套结构
        self.assertIn("TosShipperInfo", api_input)
        tos_info_data = api_input["TosShipperInfo"]
        self.assertEqual(tos_info_data["Prefix"], "test-prefix")
        self.assertEqual(tos_info_data["MaxSize"], 10)
        self.assertEqual(tos_info_data["Compress"], "gzip")
        self.assertEqual(tos_info_data["Interval"], 600)
        self.assertEqual(tos_info_data["PartitionFormat"], "%Y/%m/%d")

    def test_modify_shipper_csv_content(self):
        """测试 ModifyShipperRequest 在 CSV 内容格式下的 ContentInfo 序列化。"""
        csv_info = CsvInfo(
            keys=["field1", "field2", "field3"],
            delimiter=",",
            escape_char="\\",
            print_header=True,
            non_field_content="N/A",
        )

        content_info = ContentInfo(
            format="csv",
            csv_info=csv_info,
        )

        modify_shipper_request = ModifyShipperRequest(
            shipper_id="test-shipper-id",
            content_info=content_info,
        )

        api_input = modify_shipper_request.get_api_input()

        self.assertIn("ContentInfo", api_input)
        content_info_data = api_input["ContentInfo"]
        self.assertEqual(content_info_data["Format"], "csv")
        self.assertIn("CsvInfo", content_info_data)
        csv_info_data = content_info_data["CsvInfo"]
        self.assertEqual(csv_info_data["Keys"], ["field1", "field2", "field3"])
        self.assertEqual(csv_info_data["Delimiter"], ",")
        self.assertEqual(csv_info_data["EscapeChar"], "\\")
        self.assertEqual(csv_info_data["PrintHeader"], True)
        self.assertEqual(csv_info_data["NonFieldContent"], "N/A")

    def test_modify_shipper_kafka_content(self):
        """测试 ModifyShipperRequest 中 KafkaShipperInfo 序列化。"""
        kafka_shipper_info = KafkaShipperInfo(
            instance="kafka-instance-123",
            kafka_topic="test-topic",
            compress="lz4",
            start_time=1640995200000,  # 2022-01-01 00:00:00 UTC
            end_time=1643673600000,  # 2022-02-01 00:00:00 UTC
        )

        modify_shipper_request = ModifyShipperRequest(
            shipper_id="test-shipper-id",
            shipper_type="kafka",
            kafka_shipper_info=kafka_shipper_info,
        )

        api_input = modify_shipper_request.get_api_input()

        self.assertIn("KafkaShipperInfo", api_input)
        kafka_info_data = api_input["KafkaShipperInfo"]
        self.assertEqual(kafka_info_data["Instance"], "kafka-instance-123")
        self.assertEqual(kafka_info_data["KafkaTopic"], "test-topic")
        self.assertEqual(kafka_info_data["Compress"], "lz4")
        self.assertEqual(kafka_info_data["StartTime"], 1640995200000)
        self.assertEqual(kafka_info_data["EndTime"], 1643673600000)

    @patch("volcengine.tls.TLSService.TLSService._TLSService__request")
    def test_modify_shipper_service_call(self, mock_request):
        """测试 TLSService.modify_shipper 调用的 API 名称与请求体结构。"""
        content_info = ContentInfo(
            format="json",
            json_info=JsonInfo(enable=True),
        )
        tos_shipper_info = TosShipperInfo(
            prefix="test-prefix",
            max_size=5,
            compress="snappy",
            interval=300,
            partition_format="%Y/%m/%d/%H/%M",
        )

        request = ModifyShipperRequest(
            shipper_id="shipper-123",
            shipper_name="shipper-name",
            shipper_type="tos",
            status=True,
            content_info=content_info,
            tos_shipper_info=tos_shipper_info,
            role_trn="trn:iam::123456789012:role/test-role",
            service_trn="trn:iam::123456789012:role/service-role",
        )

        mock_response = Mock()
        mock_response.headers = {
            "X-Tls-Requestid": "test-request-id",
            "Content-Type": "application/json",
        }
        mock_response.text = "{}"
        mock_request.return_value = mock_response

        response = self.tls_service.modify_shipper(request)

        expected_body = request.get_api_input()
        mock_request.assert_called_once_with(api="/ModifyShipper", body=expected_body)
        self.assertIsInstance(response, ModifyShipperResponse)
        self.assertEqual(response.get_request_id(), "test-request-id")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
