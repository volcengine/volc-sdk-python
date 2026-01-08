# coding=utf-8
# pylint: disable=no-member

import unittest

from volcengine.tls.data import AlarmNotifyGroupInfo


class TestDescribeAlarmNotifyGroupsData(unittest.TestCase):

    def test_parse_notice_rules_and_receivers(self):
        """验证 DescribeAlarmNotifyGroups 响应中 NoticeRules 和 Receivers 的解析逻辑"""
        receiver_payload = {
            "ReceiverType": "User",
            "ReceiverNames": ["user-a", "user-b"],
            "ReceiverChannels": ["Email", "GeneralWebhook"],
            "StartTime": "00:00",
            "EndTime": "23:59",
            "Webhook": "https://example-webhook",
            "GeneralWebhookUrl": "https://example.com/hook",
            "GeneralWebhookBody": "{\"msg\":\"test\"}",
            "AlarmWebhookAtUsers": ["user-a"],
            "AlarmWebhookIsAtAll": False,
            "AlarmWebhookAtGroups": ["group-1"],
            "GeneralWebhookMethod": "POST",
            "GeneralWebhookHeaders": [
                {"Key": "X-Test-Header", "Value": "value"},
            ],
            "AlarmContentTemplateId": "tpl-001",
            "AlarmWebhookIntegrationId": "wh-001",
            "AlarmWebhookIntegrationName": "integration-name",
        }

        response_data = {
            "AlarmNotifyGroupName": "python-sdk-test-notify-group",
            "AlarmNotifyGroupId": "group-id-123",
            "NotifyType": ["Trigger", "Recovery"],
            "Receivers": [receiver_payload],
            "NoticeRules": [
                {
                    "HasNext": False,
                    "HasEndNode": True,
                    "RuleNode": {
                        "Type": "Condition",
                        "Value": ["severity = 'critical'"],
                        "Children": [],
                    },
                    "ReceiverInfos": [receiver_payload],
                }
            ],
            "CreateTime": "2025-01-01 00:00:00",
            "ModifyTime": "2025-01-01 00:10:00",
            "IamProjectName": "default",
        }

        info: AlarmNotifyGroupInfo = AlarmNotifyGroupInfo.set_attributes(response_data)

        # 基本字段
        self.assertEqual(info.get_alarm_notify_group_name(), "python-sdk-test-notify-group")
        self.assertEqual(info.get_alarm_notify_group_id(), "group-id-123")
        self.assertEqual(info.get_iam_project_name(), "default")

        # Receivers 解析
        receivers = info.get_receivers()
        self.assertEqual(len(receivers), 1)
        receiver = receivers[0]
        self.assertEqual(receiver.get_receiver_type(), "User")
        self.assertEqual(receiver.get_receiver_names(), ["user-a", "user-b"])
        self.assertEqual(receiver.get_general_webhook_url(), "https://example.com/hook")
        self.assertEqual(receiver.get_alarm_webhook_at_users(), ["user-a"])
        self.assertEqual(receiver.get_alarm_webhook_is_at_all(), False)
        self.assertEqual(receiver.get_alarm_webhook_at_groups(), ["group-1"])

        headers = receiver.get_general_webhook_headers()
        self.assertEqual(len(headers), 1)
        self.assertEqual(headers[0].get_key(), "X-Test-Header")
        self.assertEqual(headers[0].get_value(), "value")

        # NoticeRules 解析
        notice_rules = info.get_notice_rules()
        self.assertEqual(len(notice_rules), 1)
        rule = notice_rules[0]
        self.assertFalse(rule.get_has_next())
        self.assertTrue(rule.get_has_end_node())

        rule_node = rule.get_rule_node()
        self.assertIsNotNone(rule_node)
        self.assertEqual(rule_node.get_type(), "Condition")
        self.assertEqual(rule_node.get_value(), ["severity = 'critical'"])
        self.assertEqual(rule_node.get_children(), [])

        rule_receivers = rule.get_receiver_infos()
        self.assertEqual(len(rule_receivers), 1)
        self.assertEqual(rule_receivers[0].get_general_webhook_url(), "https://example.com/hook")


if __name__ == "__main__":
    unittest.main()
