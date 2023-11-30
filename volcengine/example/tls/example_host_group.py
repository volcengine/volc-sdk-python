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
    now = str(int(time.time()))

    # 创建机器组
    # 请根据您的需要，填写host_group_name、host_group_type和host_ip_list等参数
    # CreateHostGroup API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112206
    create_host_group_request = CreateHostGroupRequest(host_group_name="host-group-name-" + now, host_group_type="IP",
                                                       host_ip_list=["192.168.1.1", "192.168.1.2", "192.168.1.3"])
    create_host_group_response = tls_service.create_host_group(create_host_group_request)
    host_group_id = create_host_group_response.get_host_group_id()

    # 获取指定机器组信息
    # 请根据您的需要，填写待查询的host_group_id
    # DescribeHostGroup API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112210
    describe_host_group_request = DescribeHostGroupRequest(host_group_id)
    describe_host_group_response = tls_service.describe_host_group(describe_host_group_request)
    print("host group name: {}".format(
        describe_host_group_response.get_host_group_hosts_rules_info().get_host_group_info().get_host_group_name()))
    print("first host ip: {}".format(
        describe_host_group_response.get_host_group_hosts_rules_info().get_host_infos()[0].get_ip()))

    # 获取全部机器组信息
    # 请根据您的需要，填写host_group_name等可选参数
    # DescribeHostGroups API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112211
    describe_host_groups_request = DescribeHostGroupsRequest()
    describe_host_groups_response = tls_service.describe_host_groups(describe_host_groups_request)
    print("first host group name: {}".format(
        describe_host_groups_response.get_host_group_hosts_rules_infos()[0].get_host_group_info().get_host_group_name()))
    print("first host ip: {}".format(
        describe_host_groups_response.get_host_group_hosts_rules_infos()[0].get_host_infos()[0].get_ip()))

    # 修改机器组
    # 请根据您的需要，填写host_group_id和待修改的机器组信息
    # ModifyHostGroup API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112209
    modify_host_group_request = ModifyHostGroupRequest(host_group_id, host_group_name="change-host-group-name-" + now)
    modify_host_group_response = tls_service.modify_host_group(modify_host_group_request)

    # 查询机器组所有机器
    # 请根据您的需要，填写待查询的host_group_id
    # DescribeHosts API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112212
    describe_hosts_request = DescribeHostsRequest(host_group_id)
    describe_hosts_response = tls_service.describe_hosts(describe_hosts_request)
    print("total {} hosts\nfirst host ip: {}".format(describe_hosts_response.get_total(),
                                                     describe_hosts_response.get_host_infos()[0].get_ip()))

    # 删除机器组内指定机器
    # 请根据您的需要，填写待删除机器的host_group_id和ip
    # DeleteHost API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112213
    delete_host_request = DeleteHostRequest(host_group_id, ip="192.168.1.3")
    delete_host_response = tls_service.delete_host(delete_host_request)

    # 查询机器组的采集配置
    # 请根据您的需要，填写待查询的host_group_id
    # DescribeHostGroupRules API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112214
    describe_host_group_rules_request = DescribeHostGroupRulesRequest(host_group_id)
    describe_host_group_rules_response = tls_service.describe_host_group_rules(describe_host_group_rules_request)
    print("total {} hosts".format(describe_host_group_rules_response.get_total()))

    # 删除机器组
    # 请根据您的需要，填写待删除的host_group_id
    # DeleteHostGroup API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112208
    delete_host_group_request = DeleteHostGroupRequest(host_group_id)
    delete_host_group_response = tls_service.delete_host_group(delete_host_group_request)
