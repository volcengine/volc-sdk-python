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

    # 查询指定日志项目信息
    describe_project_request = DescribeProjectRequest(project_id)
    describe_project_response = tls_service.describe_project(describe_project_request)

    # 查询所有日志项目信息
    describe_projects_request = DescribeProjectsRequest()
    describe_projects_response = tls_service.describe_projects(describe_projects_request)

    # 修改日志项目
    modify_project_request = ModifyProjectRequest(project_id, project_name="change-project-name",
                                                  description="change-project-description")
    modify_project_response = tls_service.modify_project(modify_project_request)

    # 删除日志项目
    delete_project_request = DeleteProjectRequest(project_id)
    delete_project_response = tls_service.delete_project(delete_project_request)
