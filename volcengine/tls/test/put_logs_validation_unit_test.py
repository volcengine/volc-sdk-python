import unittest

from volcengine.tls.log_pb2 import LogGroupList, LogGroup, Log
from volcengine.tls.tls_requests import PutLogsRequest


class PutLogsValidationUnitTest(unittest.TestCase):
    def _make_group(self, count):
        group = LogGroup()
        for _ in range(count):
            group.logs.append(Log())
        return group

    def test_log_group_count_validation(self):
        log_group_list = LogGroupList()
        log_group_list.log_groups.append(self._make_group(10000))
        request = PutLogsRequest("topic", log_group_list)
        self.assertTrue(request.check_validation())

        log_group_list = LogGroupList()
        log_group_list.log_groups.append(self._make_group(10001))
        request = PutLogsRequest("topic", log_group_list)
        self.assertFalse(request.check_validation())


if __name__ == "__main__":
    unittest.main()
