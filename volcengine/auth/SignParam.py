# coding:utf-8
import datetime
from collections import OrderedDict


class SignParam(object):
    def __init__(self):
        self.body = ''
        self.query = OrderedDict()
        self.date = datetime.datetime.now()
        self.header_list = OrderedDict()
        self.is_sign_url = False
        self.host = ''
        self.path = '/'
        self.method = ''

    def set_date(self, date):
        self.date = date

    def set_body(self, body):
        self.body = body

    def set_host(self, host):
        self.host = host

    def set_query(self, query):
        self.query = query

    def set_header_list(self, header_list):
        self.header_list = header_list

    def set_is_sign_url(self, is_sign_url):
        self.is_sign_url = is_sign_url

    def set_path(self, path):
        self.path = path

    def set_method(self, method):
        self.method = method




