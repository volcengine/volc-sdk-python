# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import DescribeTraceInstanceRequest


if __name__ == "__main__":
    # 初始化TLS服务
    endpoint = "your-endpoint"
    access_key_id = "your-access-key-id"
    access_key_secret = "your-access-key-secret"
    region = "your-region"

    tls_service = TLSService(endpoint, access_key_id, access_key_secret, region)

    # 创建DescribeTraceInstance请求
    trace_instance_id = "your-trace-instance-id"
    request = DescribeTraceInstanceRequest(trace_instance_id=trace_instance_id)

    try:
        # 调用DescribeTraceInstance API
        response = tls_service.describe_trace_instance(request)
        
        # 获取Trace实例信息
        trace_instance = response.get_trace_instance()
        
        print(f"Trace Instance ID: {trace_instance.get_trace_instance_id()}")
        print(f"Trace Instance Name: {trace_instance.get_trace_instance_name()}")
        print(f"Trace Instance Status: {trace_instance.get_trace_instance_status()}")
        print(f"Project ID: {trace_instance.get_project_id()}")
        print(f"Project Name: {trace_instance.get_project_name()}")
        print(f"Description: {trace_instance.get_description()}")
        print(f"Create Time: {trace_instance.get_create_time()}")
        print(f"Modify Time: {trace_instance.get_modify_time()}")
        print(f"Trace Topic ID: {trace_instance.get_trace_topic_id()}")
        print(f"Trace Topic Name: {trace_instance.get_trace_topic_name()}")
        print(f"Dependency Topic ID: {trace_instance.get_dependency_topic_id()}")
        print(f"Dependency Topic Name: {trace_instance.get_dependency_topic_topic_name()}")
        
    except Exception as e:
        print(f"Error: {e}")