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
    # 请根据您的需要，填写project_name和可选的description；请您填写和初始化tls_service时一致的region
    # CreateProject API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112174
    create_project_request = CreateProjectRequest(project_name="project-name-" + now, region=region,
                                                  description="project-description")
    create_project_response = tls_service.create_project(create_project_request)
    project_id = create_project_response.get_project_id()

    # 查询指定日志项目信息
    # 请根据您的需要，填写待查询的project_id
    # DescribeProject API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112178
    describe_project_request = DescribeProjectRequest(project_id)
    describe_project_response = tls_service.describe_project(describe_project_request)
    project = describe_project_response.get_project()
    print("project id: {}".format(project.get_project_id()))

    # 查询所有日志项目信息
    # 请根据您的需要，填写project_name等参数
    # DescribeProjects API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112179
    describe_projects_request = DescribeProjectsRequest()
    describe_projects_response = tls_service.describe_projects(describe_projects_request)
    print("project total: {}\nfirst project name: {}".format(describe_projects_response.get_total(),
                                                             describe_projects_response.get_projects()[0].get_project_name()))

    # 修改日志项目
    # 请根据您的需要，填写project_name或description等参数
    # ModifyProject API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112177
    modify_project_request = ModifyProjectRequest(project_id, project_name="change-project-name",
                                                  description="change-project-description")
    modify_project_response = tls_service.modify_project(modify_project_request)

    # 删除日志项目
    # 请根据您的需要，填写待删除的project_id
    # DeleteProject API的请求参数规范请参阅 https://www.volcengine.com/docs/6470/112176
    delete_project_request = DeleteProjectRequest(project_id)
    delete_project_response = tls_service.delete_project(delete_project_request)
