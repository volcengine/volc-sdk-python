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

    # 创建告警组
    # 请根据您的需要，填写alarm_notify_group_name、notify_type和receivers等参数
    # CreateAlarmNotifyGroup API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112220
    receiver = Receiver(receiver_type="User", receiver_names=["chenlei_test_sy_7_subuser1"], receiver_channels=["Email", "Sms"],
                        start_time="00:00:00", end_time="23:59:59")
    create_alarm_notify_group_request = CreateAlarmNotifyGroupRequest(
        alarm_notify_group_name="alarm-notify-group-name-" + now,
        notify_type=["Trigger", "Recovery"],
        receivers=[receiver],)
    create_alarm_notify_group_response = tls_service.create_alarm_notify_group(create_alarm_notify_group_request)
    alarm_notify_group_id = create_alarm_notify_group_response.get_alarm_notify_group_id()

    # 获取不存在告警组的测试
    # 请根据您的需要，填写alarm_notify_group_name等参数
    # DescribeAlarmNotifyGroups API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112223
    describe_alarm_notify_groups_request = DescribeAlarmNotifyGroupsRequest(alarm_notify_group_id="no-exists-notify-group-id" + now,)
    describe_alarm_notify_groups_response = tls_service.describe_alarm_notify_groups(
        describe_alarm_notify_groups_request)
    print("topics total: {}\n" . format(describe_alarm_notify_groups_response.get_total()))

    # 获取告警组
    # 请根据您的需要，填写alarm_notify_group_name等参数
    # DescribeAlarmNotifyGroups API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112223
    describe_alarm_notify_groups_request = DescribeAlarmNotifyGroupsRequest()
    describe_alarm_notify_groups_response = tls_service.describe_alarm_notify_groups(
        describe_alarm_notify_groups_request)
    print("topics total: {}\nfirst alarm group name: {}".format(describe_alarm_notify_groups_response.get_total(),
                                                                describe_alarm_notify_groups_response.
                                                                get_alarm_notify_groups()[0].get_alarm_notify_group_name()))

    # 修改告警组
    # 请根据您的需要，填写待修改的alarm_notify_group_id和其它参数
    # ModifyAlarmNotifyGroup API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112222
    modify_alarm_notify_group_request = \
        ModifyAlarmNotifyGroupRequest(alarm_notify_group_id,
                                      alarm_notify_group_name="change-alarm-notify-group-name-" + now)
    modify_alarm_notify_group_response = tls_service.modify_alarm_notify_group(modify_alarm_notify_group_request)

    # 创建告警策略
    # 请根据您的需要，填写project_id、alarm_name、query_request、request_cycle、condition、alarm_period、alarm_notify_group等参数
    # CreateAlarm API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112216
    query_request = QueryRequest(topic_id=topic_id, query="Failed | select count(*) as errNum", number=1,
                                 start_time_offset=-15, end_time_offset=0, time_span_type="Relative",
                                 truncated_time="Minute")
    request_cycle = RequestCycle(cycle_type="Period", time=10)
    trigger_conditions = [TriggerCondition(condition="$1.errNum>=5", severity="warning")]
    create_alarm_request = CreateAlarmRequest(project_id, alarm_name="alarm-name", query_request=[query_request],
                                              request_cycle=request_cycle, condition="$1.errNum>0", alarm_period=60,
                                              alarm_notify_group=[alarm_notify_group_id],
                                              trigger_conditions=trigger_conditions)
    create_alarm_response = tls_service.create_alarm(create_alarm_request)
    alarm_id = create_alarm_response.alarm_id

    # 创建告警策略 - 关联检索分析结果
    # 请根据您的需要，填写project_id、alarm_name、query_request、request_cycle、condition、alarm_period、alarm_notify_group等参数
    # CreateAlarm API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112216
    query_request_1 = QueryRequest(topic_id=topic_id, query="Failed | select count(*) as errCount", number=1,
                                 start_time_offset=-15, end_time_offset=0)
    query_request_2 = QueryRequest(topic_id=topic_id, query="Error | select count(*) as errCount", number=2,
                                 start_time_offset=-15, end_time_offset=0)
    request_cycle = RequestCycle(cycle_type="Period", time=10)
    join_configurations = [JoinConfig(set_operation_type="CrossJoin", condition="")]
    trigger_conditions = [TriggerCondition(condition="$1.errCount + $2.errCount >= 10", severity="warning")]
    create_alarm_request = CreateAlarmRequest(project_id, alarm_name="alarm-name-with-join-configurations", query_request=[query_request_1, query_request_2],
                                              request_cycle=request_cycle, condition="", alarm_period=60,
                                              alarm_notify_group=[alarm_notify_group_id],
                                              join_configurations=join_configurations,
                                              trigger_conditions=trigger_conditions)
    create_alarm_response = tls_service.create_alarm(create_alarm_request)
    alarm_id_2 = create_alarm_response.alarm_id

    # 修改告警策略
    # 请根据您的需要，填写待修改的alarm_id和其它参数
    # ModifyAlarm API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112218
    trigger_conditions = [TriggerCondition(condition="$1.errNum>=6", severity="warning")]
    query_request = QueryRequest(topic_id=topic_id, query="Failed | select count(*) as errNum", number=1,
                                 start_time_offset=-15, end_time_offset=0, time_span_type="Today",
                                 truncated_time="Hour")
    modify_alarm_request = ModifyAlarmRequest(alarm_id, trigger_period=2, trigger_conditions=trigger_conditions,
                                              query_request=[query_request])
    modify_alarm_response = tls_service.modify_alarm(modify_alarm_request)

    # 查询告警策略
    # 请根据您的需要，填写待查询的project_id
    # DescribeAlarms API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112219
    describe_alarms_request = DescribeAlarmsRequest(project_id)
    describe_alarms_response = tls_service.describe_alarms(describe_alarms_request)
    print("topics total:{} first alarm name:{}".format(describe_alarms_response.get_total(),
                                                       describe_alarms_response.get_alarms()[0].get_alarm_name()))

    # 删除告警策略
    # 请根据您的需要，填写待删除的alarm_id
    # DeleteAlarm API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112217
    delete_alarm_request = DeleteAlarmRequest(alarm_id)
    delete_alarm_response = tls_service.delete_alarm(delete_alarm_request)

    tls_service.delete_alarm(DeleteAlarmRequest(alarm_id_2))

    # 删除告警组
    # 请根据您的需要，填写待删除的alarm_notify_group_id
    # DeleteAlarmNotifyGroup API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112221
    delete_alarm_notify_group_request = DeleteAlarmNotifyGroupRequest(alarm_notify_group_id)
    delete_alarm_notify_group_response = tls_service.delete_alarm_notify_group(delete_alarm_notify_group_request)

    # 删除日志主题
    tls_service.delete_topic(DeleteTopicRequest(topic_id))

    # 删除日志项目
    tls_service.delete_project(DeleteProjectRequest(project_id))
