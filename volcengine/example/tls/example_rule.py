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

    # 创建日志项目
    create_project_request = CreateProjectRequest(project_name="project-name-" + now, region=region,
                                                  description="project-description")
    create_project_response = tls_service.create_project(create_project_request)
    project_id = create_project_response.get_project_id()

    # 创建日志主题
    create_topic_request = CreateTopicRequest(topic_name="topic-name-" + now, project_id=project_id,
                                              ttl=3650, description="topic-description", shard_count=2)
    create_topic_response = tls_service.create_topic(create_topic_request)
    topic_id = create_topic_response.get_topic_id()

    # 创建采集配置
    # 请根据您的需要，填写topic_id、rule_name和其它采集配置参数
    # CreateRule API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112199
    rule_name = "rule-name"
    paths = ["/data/nginx/log/*/*/*.log"]
    log_type = "delimiter_log"
    extract_rule = ExtractRule(delimiter="#", keys=["time", "level", "msg"],
                               time_key="time", time_format="%Y-%m-%dT%H:%M:%S,%f",
                               filter_key_regex=[FilterKeyRegex("msg", ".*ERROR.*")],
                               un_match_up_load_switch=True, un_match_log_key="LogParseFailed")
    exclude_paths = [ExcludePath("File", "/data/nginx/log/*/*/exclude.log"),
                     ExcludePath("Path", "/data/nginx/log/*/exclude/")]
    user_define_rule = UserDefineRule(ParsePathRule(path_sample="/var/logs/instanceid_any_podname/test.log",
                                                    regex="\\/var\\/logs\\/([a-z]*)_any_([a-z]*)\\/test\\.log",
                                                    keys=["instance-id", "pod-name"]))
    log_sample = "2018-05-22 15:35:53.850#INFO#XXXX"
    input_type = 2
    container_rule = ContainerRule(container_name_regex=".*Name.*",
                                   include_container_label_regex={"Key1": "Value1", "Key2": "Value2"},
                                   exclude_container_label_regex={"Key1": "Value1", "Key2": "Value2"},
                                   include_container_env_regex={"Key1": "Value1", "Key2": "Value2"},
                                   exclude_container_env_regex={"Key1": "Value1", "Key2": "Value2"},
                                   env_tag={"Key1": "Value1", "Key2": "Value2"},
                                   kubernetes_rule=KubernetesRule(namespace_name_regex=".*Name.*",
                                                                  workload_type="Deployment",
                                                                  workload_name_regex=".*workload.*",
                                                                  include_pod_label_regex={"Key1": "Value1",
                                                                                           "Key2": "Value2"},
                                                                  exclude_pod_label_regex={"Key1": "Value1",
                                                                                           "Key2": "Value2"},
                                                                  pod_name_regex=".*Name.*",
                                                                  label_tag={"Key1": "Value1", "Key2": "Value2"}))
    create_rule_request = CreateRuleRequest(topic_id, rule_name, paths, log_type, extract_rule, exclude_paths,
                                            user_define_rule, log_sample, input_type, container_rule)
    create_rule_response = tls_service.create_rule(create_rule_request)
    rule_id = create_rule_response.get_rule_id()

    # 查询指定采集配置
    # 请根据您的需要，填写待查询的rule_id
    # DescribeRule API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112202
    describe_rule_request = DescribeRuleRequest(rule_id)
    describe_rule_response = tls_service.describe_rule(describe_rule_request)
    print("rule name: {}".format(describe_rule_response.get_rule_info().get_rule_name()))

    # 查询日志项目所有采集配置
    # 请根据您的需要，填写待查询的project_id
    # DescribeRules API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112203
    describe_rules_request = DescribeRulesRequest(project_id)
    describe_rules_response = tls_service.describe_rules(describe_rules_request)
    print("topics total:{}\nfirst rule name: {}".format(describe_rules_response.get_total(),
                                                      describe_rules_response.get_rule_infos()[0].get_rule_name()))

    # 修改采集配置
    # 请根据您的需要，填写待修改的rule_id、rule_name或其它参数
    # ModifyRule API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112201
    modify_rule_request = ModifyRuleRequest(rule_id, rule_name="change-rule-name-" + now)
    modify_rule_response = tls_service.modify_rule(modify_rule_request)

    # 创建机器组
    create_host_group_request = CreateHostGroupRequest(host_group_name="host-group-name", host_group_type="IP",
                                                       host_ip_list=["192.168.1.1", "192.168.1.2", "192.168.1.3"])
    create_host_group_response = tls_service.create_host_group(create_host_group_request)
    host_group_id = create_host_group_response.get_host_group_id()

    # 应用采集配置到机器组
    # 请根据您的需要，填写rule_id和host_group_ids列表
    # ApplyRuleToHostGroups API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112204
    apply_rule_to_host_groups_request = ApplyRuleToHostGroupsRequest(rule_id, host_group_ids=[host_group_id])
    apply_rule_to_host_groups_response = tls_service.apply_rule_to_host_groups(apply_rule_to_host_groups_request)

    # 删除机器组的采集配置
    # 请根据您的需要，填写rule_id和host_group_ids列表
    # DeleteRuleFromHostGroups API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112205
    delete_rule_from_host_groups_request = DeleteRuleFromHostGroupsRequest(rule_id, host_group_ids=[host_group_id])
    delete_rule_from_host_groups_response = tls_service.delete_rule_from_host_groups(
        delete_rule_from_host_groups_request)

    # 删除采集配置
    # 请根据您的需要，填写待删除的rule_id
    # DeleteRule API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112200
    delete_rule_request = DeleteRuleRequest(rule_id)
    delete_rule_response = tls_service.delete_rule(delete_rule_request)

    # 删除日志主题
    tls_service.delete_topic(DeleteTopicRequest(topic_id))

    # 删除日志项目
    tls_service.delete_project(DeleteProjectRequest(project_id))
