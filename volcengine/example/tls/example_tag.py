# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import *


if __name__ == "__main__":
    # 初始化客户端，推荐通过环境变量动态获取火山引擎密钥等身份认证信息，以免AccessKey硬编码引发数据安全风险。详细说明请参考 https://www.volcengine.com/docs/6470/1166455
    # 使用STS时，ak和sk均使用临时密钥，且设置VOLCENGINE_TOKEN；不使用STS时，VOLCENGINE_TOKEN部分传空
    endpoint = os.environ["VOLCENGINE_ENDPOINT"]
    region = os.environ["VOLCENGINE_REGION"]
    access_key_id = os.environ["VOLCENGINE_ACCESS_KEY_ID"]
    access_key_secret = os.environ["VOLCENGINE_ACCESS_KEY_SECRET"]

    # 实例化TLS客户端
    tls_service = TLSService(endpoint, access_key_id, access_key_secret, region)

    # 为日志项目或日志主题绑定标签
    # 请根据您的需要，填写resource_type、resource_list和tags等参数
    # AddTagsToResource API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/597772
    add_tags_to_resource_req = AddTagsToResourceRequest(resource_type="topic",
                                                        resources_list=["your-topic-id-1", "your-topic-id-2"],
                                                        tags=[TagInfo("test-tag-key", "test-tag-value")])
    add_tags_to_resource_resp = tls_service.add_tags_to_resource(add_tags_to_resource_req)

    # 为日志项目或日志主题解绑标签
    # 请根据您的需要，填写resource_type、resource_list和tag_key_list等参数
    # RemoveTagsFromResource API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/597802
    remove_tags_from_resource_req = RemoveTagsFromResourceRequest(resource_type="topic",
                                                                  resources_list=["your-topic-id"],
                                                                  tag_key_list=["test-tag-key"])
    remove_tags_from_resource_resp = tls_service.remove_tags_from_resource(remove_tags_from_resource_req)
