# coding: utf-8
import json
import logging
import os
import time
from collections import OrderedDict

from requests.auth import AuthBase

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

try:
    import configparser as configparser
except ImportError:
    import ConfigParser as configparser

import requests

from volcengine.Policy import SecurityToken2, InnerToken, ComplexEncoder
from volcengine.auth.SignerV4 import SignerV4
from volcengine.base.Request import Request
from volcengine.util.Util import *
from volcengine import VERSION


class VolcAuth(AuthBase):
    def __init__(self, client, request):
        # setup any auth-related data here
        self.client = client
        self.request = request

    def __call__(self, r):
        self.request.body = r.body
        if "Content-Type" in r.headers:
            self.request.headers["Content-Type"] = r.headers["Content-Type"]
        if "Content-Length" in r.headers:
            self.request.headers["Content-Length"] = r.headers["Content-Length"]
        SignerV4.sign(self.request, self.client.service_info.credentials)
        for k in self.request.headers:
            v = self.request.headers[k]
            r.headers[k] = v
        return r.headers


class Service(object):
    def __init__(self, service_info, api_info):
        self.service_info = service_info
        self.api_info = api_info
        self.session = requests.session()
        self.init()

    def init(self):
        if 'VOLC_ACCESSKEY' in os.environ and 'VOLC_SECRETKEY' in os.environ:
            self.service_info.credentials.set_ak(os.environ['VOLC_ACCESSKEY'])
            self.service_info.credentials.set_sk(os.environ['VOLC_SECRETKEY'])
        else:
            if os.environ.get('HOME', None) is None:
                return
            # 先尝试从credentials中读取ak、sk，credentials不存在则从config中读取
            path_ini = os.environ['HOME'] + '/.volc/credentials'
            path_json = os.environ['HOME'] + '/.volc/config'
            if os.path.isfile(path_ini):
                conf = configparser.ConfigParser()
                conf.read(path_ini)
                default_section, ak_option, sk_option = "default", "access_key_id", "secret_access_key"
                if conf.has_section(default_section):
                    if conf.has_option(default_section, ak_option):
                        ak = conf.get(default_section, ak_option)
                        self.service_info.credentials.set_ak(ak)
                    if conf.has_option(default_section, sk_option):
                        sk = conf.get(default_section, sk_option)
                        self.service_info.credentials.set_sk(sk)
            elif os.path.isfile(path_json):
                with open(path_json, 'r') as f:
                    try:
                        j = json.load(f)
                    except Exception:
                        logging.warning("%s is not json file", path_json)
                        return
                    if 'ak' in j:
                        self.service_info.credentials.set_ak(j['ak'])
                    if 'sk' in j:
                        self.service_info.credentials.set_sk(j['sk'])

    def set_ak(self, ak):
        self.service_info.credentials.set_ak(ak)

    def set_sk(self, sk):
        self.service_info.credentials.set_sk(sk)

    def set_session_token(self, session_token):
        self.service_info.credentials.set_session_token(session_token)

    def set_host(self, host):
        self.service_info.host = host

    def set_scheme(self, scheme):
        self.service_info.scheme = scheme
    
    def set_connection_timeout(self, connection_timeout):
        self.service_info.connection_timeout = connection_timeout

    def set_socket_timeout(self, socket_timeout):
        self.service_info.socket_timeout = socket_timeout

    def get_sign_url(self, api, params):
        if not (api in self.api_info):
            raise Exception("no such api")
        api_info = self.api_info[api]

        mquery = self.merge(api_info.query, params)
        r = Request()
        r.set_shema(self.service_info.scheme)
        r.set_method(api_info.method)
        r.set_path(api_info.path)
        r.set_query(mquery)

        return SignerV4.sign_url(r, self.service_info.credentials)

    def get(self, api, params, doseq=0):
        if not (api in self.api_info):
            raise Exception("no such api")
        api_info = self.api_info[api]

        r = self.prepare_request(api_info, params, doseq)

        SignerV4.sign(r, self.service_info.credentials)

        url = r.build(doseq)
        resp = self.session.get(url, headers=r.headers,
                                timeout=(self.service_info.connection_timeout, self.service_info.socket_timeout))
        if resp.status_code == 200:
            return resp.text
        else:
            raise Exception(resp.text)

    def post(self, api, params, form):
        if not (api in self.api_info):
            raise Exception("no such api")
        api_info = self.api_info[api]
        r = self.prepare_request(api_info, params)
        r.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        r.form = self.merge(api_info.form, form)
        r.body = urlencode(r.form, True)
        SignerV4.sign(r, self.service_info.credentials)

        url = r.build()

        resp = self.session.post(url, headers=r.headers, data=r.form,
                                 timeout=(self.service_info.connection_timeout, self.service_info.socket_timeout))
        if resp.status_code == 200:
            return resp.text
        else:
            raise Exception(resp.text)

    def request(self, api, params, data, files=None, reqConfig=None):

        if not (api in self.api_info):
            raise Exception("no such api")
        api_info = self.api_info[api]

        r = self.prepare_request(api_info, params)
        if reqConfig is not None:
            reqConfig(r)
        url = r.build()

        resp = self.session.request(api_info.method, url, data=data, files=files,
                                    timeout=(self.service_info.connection_timeout, self.service_info.socket_timeout),
                                    auth=VolcAuth(self, r))
        if resp.status_code == 200:
            return resp.text
        else:
            raise Exception(resp.text)

    def json(self, api, params, body):
        if not (api in self.api_info):
            raise Exception("no such api")
        api_info = self.api_info[api]
        r = self.prepare_request(api_info, params)
        r.headers['Content-Type'] = 'application/json'
        r.body = body

        SignerV4.sign(r, self.service_info.credentials)

        url = r.build()
        resp = self.session.post(url, headers=r.headers, data=r.body,
                                 timeout=(self.service_info.connection_timeout, self.service_info.socket_timeout))
        if resp.status_code == 200:
            return json.dumps(resp.json())
        else:
            raise Exception(resp.text.encode("utf-8"))

    def put(self, url, file_path, headers):
        with open(file_path, 'rb') as f:
            resp = self.session.put(url, headers=headers, data=f)
            headers["X-Tt-Logid"] = resp.headers.get("X-Tt-Logid", "")
            if resp.status_code == 200:
                return True, resp.text.encode("utf-8")
            else:
                return False, resp.text.encode("utf-8")

    def put_data(self, url, data, headers):
        resp = self.session.put(url, headers=headers, data=data)
        headers["X-Tt-Logid"] = resp.headers.get("X-Tt-Logid", "")
        if resp.status_code == 200:
            return True, resp.text.encode("utf-8")
        else:
            return False, resp.text.encode("utf-8")

    def prepare_request(self, api_info, params, doseq=0):
        for key in params:
            if type(params[key]) == int or type(params[key]) == float or type(params[key]) == bool:
                params[key] = str(params[key])
            elif sys.version_info[0] != 3:
                if type(params[key]) == unicode:
                    params[key] = params[key].encode('utf-8')
            elif type(params[key]) == list:
                if not doseq:
                    params[key] = ','.join(params[key])

        connection_timeout = self.service_info.connection_timeout
        socket_timeout = self.service_info.socket_timeout

        r = Request()
        r.set_shema(self.service_info.scheme)
        r.set_method(api_info.method)
        r.set_connection_timeout(connection_timeout)
        r.set_socket_timeout(socket_timeout)

        mheaders = self.merge(api_info.header, self.service_info.header)
        mheaders['Host'] = self.service_info.host
        mheaders['User-Agent'] = 'volc-sdk-python/' + VERSION
        r.set_headers(mheaders)

        mquery = self.merge(api_info.query, params)
        r.set_query(mquery)

        r.set_host(self.service_info.host)
        r.set_path(api_info.path)

        return r

    def merge(self, param1, param2):
        od = OrderedDict()
        for key in param1:
            od[key] = param1[key]

        for key in param2:
            od[key] = param2[key]

        return od

    def sign_sts2(self, policy, expire):
        sk = self.service_info.credentials.sk
        key = hashlib.md5(sk.encode('utf-8')).digest()

        sts = SecurityToken2()
        sts.access_key_id = Util.generate_access_key_id('AKTP')
        sts.secret_access_key = Util.generate_secret_key()
        now = int(time.time())
        sts.current_time = Service.to_rfc3339(now)

        if expire < 60:
            expire = 60
        expire = now + expire
        sts.expired_time = Service.to_rfc3339(expire)

        inner_token = InnerToken()
        inner_token.lt_access_key_id = self.service_info.credentials.ak
        inner_token.access_key_id = sts.access_key_id
        if policy is None:
            inner_token.policy_string = ''
        else:
            inner_token.policy_string = json.dumps(
                policy, cls=ComplexEncoder, sort_keys=True).replace(' ', '')
        inner_token.signed_secret_access_key = Util.aes_encrypt_cbc_with_base64(
            sts.secret_access_key, key)
        inner_token.expired_time = expire

        sign_str = '{}|{}|{}|{}|{}'.format(inner_token.lt_access_key_id, inner_token.access_key_id,
                                           inner_token.expired_time, inner_token.signed_secret_access_key,
                                           inner_token.policy_string)
        inner_token.signature = Util.to_hex(Util.hmac_sha256(key, sign_str))

        sts.session_token = 'STS2' + base64.b64encode(
            json.dumps(inner_token, cls=ComplexEncoder, sort_keys=True).replace(' ', '').encode('utf-8')).decode()
        return sts

    @staticmethod
    def to_rfc3339(t):
        format_time = time.strftime('%Y-%m-%dT%H:%M:%S%z', time.localtime(t))
        pos = format_time.find('+')
        if pos == -1:
            pos = format_time.find('-')
        return format_time[:pos + 3] + ':' + format_time[pos + 3:pos + 5]
