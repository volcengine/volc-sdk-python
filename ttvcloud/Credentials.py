# coding:utf-8


class Credentials(object):
    def __init__(self, ak, sk, service, region):
        self.ak = ak
        self.sk = sk
        self.service = service
        self.region = region

    def set_ak(self, ak):
        self.ak = ak

    def set_sk(self, sk):
        self.sk = sk
