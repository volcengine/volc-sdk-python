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

    # 创建日志项目
    create_project_request = CreateProjectRequest(project_name="project-name", region=region,
                                                  description="project-description")
    create_project_response = tls_service.create_project(create_project_request)
    project_id = create_project_response.project_id

    # 创建日志主题
    create_topic_request = CreateTopicRequest(topic_name="topic-name", project_id=project_id,
                                              ttl=3650, description="topic-description", shard_count=2)
    create_topic_response = tls_service.create_topic(create_topic_request)
    topic_id = create_topic_response.topic_id

    # 创建采集配置
    rule_name = "rule-name"
    paths = ["/data/nginx/log/*/*/*.log"]
    log_type = "delimiter_log"
    extract_rule = ExtractRule(delimiter="#", keys=["time", "", "level", "msg"],
                               time_key="time", time_format="%Y-%m-%dT%H:%M:%S,%f",
                               filter_key_regex=[FilterKeyRegex("msg", ".*ERROR.*")],
                               un_match_up_load_switch=True, un_match_log_key="LogParseFailed")
    exclude_paths = [ExcludePath("File", "/data/nginx/log/*/*/exclude.log"),
                     ExcludePath("Path", "/data/nginx/log/*/exclude/")]
    user_define_rule = UserDefineRule(ParsePathRule(path_sample="/var/logs/instanceid_any_podname/test.log",
                                                    regex="\\/var\\/logs\\/([a-z]*)_any_([a-z]*)\\/test\\.log",
                                                    keys=["instance-id", "pod-name"]))
    log_sample = "2018-05-22 15:35:53.850 INFO XXXX"
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
    rule_id = create_rule_response.rule_id

    # 查询指定采集配置
    describe_rule_request = DescribeRuleRequest(rule_id)
    describe_rule_response = tls_service.describe_rule(describe_rule_request)

    # 查询日志项目所有采集配置
    describe_rules_request = DescribeRulesRequest(project_id)
    describe_rules_response = tls_service.describe_rules(describe_rules_request)

    # 修改采集配置
    modify_rule_request = ModifyRuleRequest(rule_id, rule_name="change-rule-name")
    modify_rule_response = tls_service.modify_rule(modify_rule_request)

    # 创建机器组
    create_host_group_request = CreateHostGroupRequest(host_group_name="host-group-name", host_group_type="IP",
                                                       host_ip_list=["192.168.1.1", "192.168.1.2", "192.168.1.3"])
    create_host_group_response = tls_service.create_host_group(create_host_group_request)
    host_group_id = create_host_group_response.host_group_id

    # 应用采集配置到机器组
    apply_rule_to_host_groups_request = ApplyRuleToHostGroupsRequest(rule_id, host_group_ids=[host_group_id])
    apply_rule_to_host_groups_response = tls_service.apply_rule_to_host_groups(apply_rule_to_host_groups_request)

    # 删除机器组的采集配置
    delete_rule_from_host_groups_request = DeleteRuleFromHostGroupsRequest(rule_id, host_group_ids=[host_group_id])
    delete_rule_from_host_groups_response = tls_service.delete_rule_from_host_groups(delete_rule_from_host_groups_request)

    # 删除采集配置
    delete_rule_request = DeleteRuleRequest(rule_id)
    delete_rule_response = tls_service.delete_rule(delete_rule_request)
