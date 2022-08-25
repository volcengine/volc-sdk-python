# coding:utf-8
import json

from volcengine.live.LiveService import LiveService


# 示例 -  查询直播域名带宽数据
def example_describe_live_bandwidth_data(live_service):
    body = {
        "DomainList": ["example.com", "example2.com"],
        "StartTime": "2022-04-13T00:00:00Z",
        "EndTime": "2022-04-14T00:00:00Z",
        "Aggregation": 300,
    }
    resp = live_service.describe_live_bandwidth_data(body)
    print(resp)


# 示例 -  查询直播域名流量数据
def example_describe_live_traffic_data(live_service):
    body = {
        "DomainList": ["example.com", "example2.com"],
        "StartTime": "2022-04-13T00:00:00Z",
        "EndTime": "2022-04-14T00:00:00Z",
        "Aggregation": 300,
    }
    resp = live_service.describe_live_traffic_data(body)
    print(resp)


# 示例 - 查询95带宽
def example_describe_live_P95Peak_bandwidth_data(live_service):
    body = {
        "StartTime": "2022-04-13T00:00:00Z",
        "EndTime": "2022-04-14T00:00:00Z",
        "Aggregation": 300,
    }
    resp = live_service.describe_live_P95Peak_bandwidth_data(body)
    print(resp)


# 示例 -  查询直播域名录制用量
def example_describe_record_data(live_service):
    body = {
        "DomainList": ["example.com", "example2.com"],
        "StartTime": "2022-04-13T00:00:00Z",
        "EndTime": "2022-04-13T00:10:00Z",
        "Aggregation": 300,
    }
    resp = live_service.describe_record_data(body)
    print(resp)


# 示例 -  查询直播域名转码用量
def example_describe_transcode_data(live_service):
    body = {
        "DomainList": ["example.com", "example2.com"],
        "StartTime": "2022-03-07T00:00:00+08:00",
        "EndTime": "2022-03-08T00:00:00+08:00",
        "Aggregation": 86400,
    }
    resp = live_service.describe_transcode_data(body)
    print(resp)


# 示例 -  查询直播域名截图张数
def example_describe_snapshot_data(live_service):
    body = {
        "DomainList": ["example.com", "example2.com"],
        "StartTime": "2022-03-07T00:00:00+08:00",
        "EndTime": "2022-03-08T00:00:00+08:00",
        "Aggregation": 86400,
    }
    resp = live_service.describe_snapshot_data(body)
    print(resp)


# 示例 - 日志下载
def example_describe_live_domain_log(live_service):
    params = {
        "DomainList": ["example.com", "example2.com"],
        "StartTime": "2022-04-21T14:00:00+08:00",
        "EndTime": "2022-04-22T14:00:00+08:00",
    }
    resp = live_service.describe_live_domain_log(params)
    print(resp)


# 示例 - 查询推流监控数据
def example_describe_push_stream_metrics(live_service):
    body = {
        "Domain": "example.com",
        "App": "example_app",
        "Stream": "example_stream",
        "StartTime": "2022-04-21T00:00:00Z",
        "EndTime": "2022-04-23T23:59:59Z",
        "Aggregation": 30,
    }
    resp = live_service.describe_push_stream_metrics(body)
    print(resp)


# 示例 - 查询直播流历史在线人数
def example_describe_live_stream_sessions(live_service):
    body = {
        "Domain": "example.com",
        "App": "example",
        "Stream": "example080601",
        "ProtocolList": ["RTMP", "HTTP-FLV"],
        "StartTime": "2022-04-21T00:00:00Z",
        "EndTime": "2022-04-21T10:59:59Z",
        "Aggregation": 60,
    }
    resp = live_service.describe_live_stream_sessions(body)
    print(resp)


# 示例 -  查询域名 HTTP 返回码占比
def example_describe_play_response_status_stat(live_service):
    body = {
        "DomainList": ["example.com", "example2.com"],
        "StartTime": "2021-08-16T00:00:00Z",
        "EndTime": "2021-08-16T00:01:59Z",
        "Aggregation": 60
    }
    resp = live_service.describe_play_response_status_stat(body)
    print(resp)


# 示例 - Stream流量查询
def example_describe_live_metric_traffic_data(live_service):
    body = {
        "DomainList": ["example.com"],
        "ProtocolList": ["HTTP-FLV", "RTMP"],
        "ISPList": ["telecom"],
        "IPList": ["123.123.123.000"],
        "RegionList": [
            {
                "Area": "cn",
                "Country": "cn",
                "Province": "beijing",
            },
        ],
        "StartTime": "2022-04-13T00:00:00+08:00",
        "EndTime": "2022-04-13T12:00:00+08:00",
        "Aggregation": 300,
        "ShowDetail": True,
    }
    resp = live_service.describe_live_metric_traffic_data(body)
    print(resp)


# 示例 - Stream带宽查询
def example_describe_live_metric_bandwidth_data(live_service):
    body = {
        "DomainList": ["example.com"],
        "ProtocolList": ["HTTP-FLV", "RTMP"],
        "ISPList": ["telecom"],
        "IPList": ["123.123.123.000"],
        "RegionList": [
            {
                "Area": "cn",
                "Country": "cn",
                "Province": "beijing",
            },
        ],
        "StartTime": "2021-04-13T00:00:00+08:00",
        "EndTime": "2021-04-14T00:00:00+08:00",
        "Aggregation": 300,
        "ShowDetail": True,
    }
    resp = live_service.describe_live_metric_bandwidth_data(body)
    print(resp)


# 示例 - 拉流域名查询流列表
def example_describe_play_stream_list(live_service):
    params = {
        "Domain": "example.com",
        "StartTime": "2022-04-13T00:00:00+08:00",
        "EndTime": "2022-04-14T00:00:00+08:00",
    }
    resp = live_service.describe_play_stream_list(params)
    print(resp)


# 示例 - 拉流转推带宽查询
def example_describe_pull_to_push_bandwidth_data(live_service):
    params = {
        "DomainList": ["example.com"],
        "DstAddrTypeList": ["live","Third"],
        "StartTime": "2021-04-13T00:00:00+08:00",
        "EndTime": "2021-04-14T00:00:00+08:00",
        "Aggregation": 300,
        "ShowDetail": True
    }
    resp = live_service.describe_pull_to_push_bandwidth_data(params)
    print(resp)


# 示例 - 截图审核查询
def example_describe_live_audit_data(live_service):
    params = {
        "DomainList": ["example.com", "example2.com"],
        "DetailField": ["Domain"],
        "StartTime": "2022-07-13T00:00:00+08:00",
        "EndTime": "2022-07-14T00:00:00+08:00",
        "Aggregation": 86400,
    }
    resp = live_service.describe_live_audit_data(params)
    print(resp)


if __name__ == '__main__':
    live_service = LiveService()
    ak = ""
    sk = ""
    live_service.set_ak(ak)
    live_service.set_sk(sk)
    # 1.查询直播域名带宽数据
    example_describe_live_bandwidth_data(live_service)
    # 2.查询直播域名流量数据
    example_describe_live_traffic_data(live_service)
    # 3.查询95带宽
    example_describe_live_P95Peak_bandwidth_data(live_service)
    # 4.查询直播域名录制用量
    example_describe_record_data(live_service)
    # 5.查询直播域名转码用量
    example_describe_transcode_data(live_service)
    # 6.查询直播域名截图张数
    example_describe_snapshot_data(live_service)
    # 7.日志下载
    example_describe_live_domain_log(live_service)
    # 8.查询推流监控数据
    example_describe_push_stream_metrics(live_service)
    # 9.查询直播流历史在线人数
    example_describe_live_stream_sessions(live_service)
    # 10.查询域名 HTTP 返回码占比
    example_describe_play_response_status_stat(live_service)
    # 11.Stream流量查询
    example_describe_live_metric_traffic_data(live_service)
    # 12.Stream带宽查询
    example_describe_live_metric_bandwidth_data(live_service)
    # 13.拉流域名查询流列表
    example_describe_play_stream_list(live_service)
    # 14.拉流转推带宽查询
    example_describe_pull_to_push_bandwidth_data(live_service)
