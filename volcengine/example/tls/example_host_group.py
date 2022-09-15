# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import *


if __name__ == "__main__":
    # 请查询控制台，填写以下参数值
    endpoint = ""
    access_key_id = ""
    access_key_secret = ""
    region = ""

    # 实例化TLS客户端
    tls_service = TLSService(endpoint, access_key_id, access_key_secret, region)

    # 创建机器组
    create_host_group_request = CreateHostGroupRequest(host_group_name="host-group-name", host_group_type="IP",
                                                       host_ip_list=["192.168.1.1", "192.168.1.2", "192.168.1.3"])
    create_host_group_response = tls_service.create_host_group(create_host_group_request)
    host_group_id = create_host_group_response.host_group_id

    # 获取指定机器组信息
    describe_host_group_request = DescribeHostGroupRequest(host_group_id)
    describe_host_group_response = tls_service.describe_host_group(describe_host_group_request)

    # 获取全部机器组信息
    describe_host_groups_request = DescribeHostGroupsRequest()
    describe_host_groups_response = tls_service.describe_host_groups(describe_host_groups_request)

    # 修改机器组
    modify_host_group_request = ModifyHostGroupRequest(host_group_id, host_group_name="change-host-group-name")
    modify_host_group_response = tls_service.modify_host_group(modify_host_group_request)

    # 查询机器组所有机器
    describe_hosts_request = DescribeHostsRequest(host_group_id)
    describe_hosts_response = tls_service.describe_hosts(describe_hosts_request)

    # 删除机器组内指定机器
    delete_host_request = DeleteHostRequest(host_group_id, ip="192.168.1.3")
    delete_host_response = tls_service.delete_host(delete_host_request)

    # 查询机器组的采集配置
    describe_host_group_rules_request = DescribeHostGroupRulesRequest(host_group_id)
    describe_host_group_rules_response = tls_service.describe_host_group_rules(describe_host_group_rules_request)

    # 删除机器组
    delete_host_group_request = DeleteHostGroupRequest(host_group_id)
    delete_host_group_response = tls_service.delete_host_group(delete_host_group_request)
