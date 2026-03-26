# coding=utf-8
import os
import unittest

from volcengine.tls.TLSService import TLSService


def NewTLSService():
    required_env = ["VOLCENGINE_ENDPOINT", "VOLCENGINE_REGION", "VOLCENGINE_ACCESS_KEY_ID", "VOLCENGINE_ACCESS_KEY_SECRET"]
    if not all(os.environ.get(k) for k in required_env):
        raise unittest.SkipTest("缺少必要的环境变量，跳过 TLS 集成测试")
    return TLSService(
        endpoint=os.environ["VOLCENGINE_ENDPOINT"],
        access_key_id=os.environ["VOLCENGINE_ACCESS_KEY_ID"],
        access_key_secret=os.environ["VOLCENGINE_ACCESS_KEY_SECRET"],
        region=os.environ["VOLCENGINE_REGION"],
    )
