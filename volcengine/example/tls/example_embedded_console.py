# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import json
import requests

from urllib.parse import quote
from volcengine.sts.StsService import StsService


if __name__ == "__main__":
    # 初始化客户端，推荐通过环境变量动态获取火山引擎密钥等身份认证信息，以免AccessKey硬编码引发数据安全风险。详细说明请参考 https://www.volcengine.com/docs/6470/1166455
    access_key_id = os.environ["VOLCENGINE_ACCESS_KEY_ID"]
    access_key_secret = os.environ["VOLCENGINE_ACCESS_KEY_SECRET"]

    sts_service = StsService()
    sts_service.set_ak(access_key_id)
    sts_service.set_sk(access_key_secret)

    role_trn = "trn:iam::yourAccountID:role/yourRole"
    role_session_name = "tlsiframe"
    target_console_url = "https://console.volc-embed.com/tls/region:tls+cn-beijing"

    # 调用AssumeRole接口获取临时安全令牌
    assume_role_params = {
        "DurationSeconds": "900",
        "RoleSessionName": role_session_name,
        "RoleTrn": role_trn
    }
    assume_role_resp = sts_service.assume_role(assume_role_params)

    assume_rule_ak = assume_role_resp["Result"]["Credentials"]["AccessKeyId"]
    assume_role_sk = assume_role_resp["Result"]["Credentials"]["SecretAccessKey"]
    session_token = assume_role_resp["Result"]["Credentials"]["SessionToken"]

    # 获取登录Token
    url_str = "https://console.volc-embed.com/api/passport/login/getSigninTokenWithSTS"
    url_str = url_str + "?accessKeyId=" + quote(assume_rule_ak)
    url_str = url_str + "&secretAccessKey=" + quote(assume_role_sk)
    url_str = url_str + "&sessionToken=" + quote(session_token)
    url_str = url_str + "&sessionDuration=3600"

    get_signin_token_with_sts_resp = json.loads(requests.post(url_str).content)
    signin_token = get_signin_token_with_sts_resp["Result"]["SigninToken"]

    # 构建免密访问链接
    result = "https://console.volc-embed.com/api/passport/login/loginWithSigninToken"
    result = result + "?signinToken=" + quote(signin_token)
    result = result + '&redirectURI=' + quote(target_console_url)

    print(result)
