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

    # 创建告警组
    receiver = Receiver(receiver_type="User", receiver_names=["receiver-name"], receiver_channels=["Email", "Sms"],
                        start_time="00:00:00", end_time="23:59:59")
    create_alarm_notify_group_request = CreateAlarmNotifyGroupRequest(alarm_notify_group_name="alarm-notify-group-name",
                                                                      notify_type=["Trigger", "Recovery"],
                                                                      receivers=[receiver])
    create_alarm_notify_group_response = tls_service.create_alarm_notify_group(create_alarm_notify_group_request)
    alarm_notify_group_id = create_alarm_notify_group_response.alarm_notify_group_id

    # 获取告警组
    describe_alarm_notify_groups_request = DescribeAlarmNotifyGroupsRequest()
    describe_alarm_notify_groups_response = tls_service.describe_alarm_notify_groups(describe_alarm_notify_groups_request)

    # 修改告警组
    modify_alarm_notify_group_request = \
        ModifyAlarmNotifyGroupRequest(alarm_notify_group_id, alarm_notify_group_name="change-alarm-notify-group-name")
    modify_alarm_notify_group_response = tls_service.modify_alarm_notify_group(modify_alarm_notify_group_request)

    # 创建告警策略
    query_request = QueryRequest(topic_id=topic_id, query="Failed | select count(*) as errNum", number=1,
                                 start_time_offset=-15, end_time_offset=0)
    request_cycle = RequestCycle(cycle_type="Period", time=10)
    create_alarm_request = CreateAlarmRequest(project_id, alarm_name="alarm-name",
                                              query_request=[query_request], request_cycle=request_cycle,
                                              condition="$1.errNum>0", alarm_period=60,
                                              alarm_notify_group=[alarm_notify_group_id])
    create_alarm_response = tls_service.create_alarm(create_alarm_request)
    alarm_id = create_alarm_response.alarm_id

    # 查询告警策略
    describe_alarms_request = DescribeAlarmsRequest(project_id)
    describe_alarms_response = tls_service.describe_alarms(describe_alarms_request)

    # 修改告警策略
    modify_alarm_request = ModifyAlarmRequest(alarm_id, trigger_period=2)
    modify_alarm_response = tls_service.modify_alarm(modify_alarm_request)

    # 删除告警策略
    delete_alarm_request = DeleteAlarmRequest(alarm_id)
    delete_alarm_response = tls_service.delete_alarm(delete_alarm_request)

    # 删除告警组
    delete_alarm_notify_group_request = DeleteAlarmNotifyGroupRequest(alarm_notify_group_id)
    delete_alarm_notify_group_response = tls_service.delete_alarm_notify_group(delete_alarm_notify_group_request)
