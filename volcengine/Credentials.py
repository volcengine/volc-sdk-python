# coding:utf-8


class Credentials(object):
    def __init__(self, ak, sk, service, region, session_token=''):
        self.ak = ak
        self.sk = sk
        self.service = service
        self.region = region
        self.session_token = session_token

    def set_ak(self, ak):
        self.ak = ak

    def set_sk(self, sk):
        self.sk = sk

    def set_session_token(self, session_token):
        self.session_token = session_token
