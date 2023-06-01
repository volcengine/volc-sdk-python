# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import time

from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_requests import *

if __name__ == "__main__":
    # 请查询控制台，填写以下参数值
    endpoint = os.environ["endpoint"]
    access_key_id = os.environ["access_key_id"]
    access_key_secret = os.environ["access_key_secret"]
    region = os.environ["region"]

    # 实例化TLS客户端
    tls_service = TLSService(endpoint, access_key_id, access_key_secret, region)
    now = str(int(time.time()))
    # 创建日志项目
    create_project_request = CreateProjectRequest(project_name="project-name-" + now, region=region,
                                                  description="project-description")
    create_project_response = tls_service.create_project(create_project_request)
    project_id = create_project_response.get_project_id()

    # 查询指定日志项目信息
    describe_project_request = DescribeProjectRequest(project_id)
    describe_project_response = tls_service.describe_project(describe_project_request)
    project = describe_project_response.get_project()
    print("project id:{}".format(project.get_project_id()))

    # 查询所有日志项目信息
    describe_projects_request = DescribeProjectsRequest()
    describe_projects_response = tls_service.describe_projects(describe_projects_request)
    print("project total:{} first project name:{}".format(describe_projects_response.get_total(),
                                                          describe_projects_response.get_projects()[
                                                              0].get_project_name()))
    # 修改日志项目
    modify_project_request = ModifyProjectRequest(project_id, project_name="change-project-name",
                                                  description="change-project-description")
    modify_project_response = tls_service.modify_project(modify_project_request)

    # 删除日志项目
    delete_project_request = DeleteProjectRequest(project_id)
    delete_project_response = tls_service.delete_project(delete_project_request)
