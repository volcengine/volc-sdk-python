# coding:utf-8
from __future__ import print_function

from volcengine.sts.StsService import StsService
from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    # step1 调用AssumeRole接口获取临时ak/sk及token
    # stsService = StsService()
    # stsService.set_ak("your-ak")   # 子账号长期AK
    # stsService.set_sk("your-sk")   # 子账号长期SK
    #
    # params = {
    #     "DurationSeconds": "900",
    #     "RoleSessionName": "just_for_test",
    #     "RoleTrn": "trn:iam::yourAccountID:role/yourRole"
    # }
    #
    # print(stsService.assume_role(params))

    # step2 调用CertToken接口，绑定用户身份
    visual_service = VisualService()

    # call below method if you don't set ak and sk in $HOME/.volc/config
    visual_service.set_ak('your-sts-ak')      # sts返回的临时ak
    visual_service.set_sk('your-sts-sk')      # sts返回的临时sk
    visual_service.set_session_token('your-sts-token')  # sts返回的临时SessionToken
    # visual_service.set_host('host')

    # below shows the sdk usage for all common apis,
    # if you cannot find the needed one, please check other example files in the same dir
    # or contact us for further help

    form = {
        'req_key': 'cert_token',
        'sts_token': 'your-sts-token',
        'tos_info': {},
        'ref_source': '1',
        'liveness_type': 'motion',
        # 'ref_image': '',
        'idcard_name': '',
        'idcard_no': '',
        'liveness_timeout': 10,
        'motion_list': ['0', '1', '2', '3'],
        'fixed_motion_list': ['0'],
        'motion_count': 4,
        'max_liveness_trial': 10,
    }

    # 人脸核身Token接口
    resp = visual_service.cert_token(form)
    print(resp)

    # step3 端上集成-客户端 / h5

    # step4 调用Query接口，查询认证数据
    # visual_service = VisualService()
    #
    # # call below method if you don't set ak and sk in $HOME/.volc/config
    # visual_service.set_ak('sts-ak')      # sts返回的临时ak
    # visual_service.set_sk('sts-sk')      # sts返回的临时sk
    # visual_service.set_session_token('sts-token') # sts返回的临时SessionToken
    # # visual_service.set_host('host')
    #
    # # below shows the sdk usage for all common apis,
    # # if you cannot find the needed one, please check other example files in the same dir
    # # or contact us for further help
    #
    # # x-security-token
    # form = {
    #     'req_key': 'cert_verify_query',
    #     'byted_token': '',
    # }
    #
    # # 人脸核身Query接口
    # resp = visual_service.cert_verify_query(form)
    # print(resp)
