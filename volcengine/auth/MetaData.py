# coding:utf-8


class MetaData(object):
    def __init__(self):
        self.algorithm = ''
        self.credential_scope = ''
        self.signed_headers = ''
        self.date = ''
        self.region = ''
        self.service = ''

    def set_date(self, date):
        self.date = date

    def set_service(self, service):
        self.service = service

    def set_region(self, region):
        self.region = region

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm

    def set_credential_scope(self, credential_scope):
        self.credential_scope = credential_scope

    def set_signed_headers(self, signed_headers):
        self.signed_headers = signed_headers