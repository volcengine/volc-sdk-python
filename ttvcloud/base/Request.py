# coding : utf-8
from collections import OrderedDict

try:
    from urllib import urlencode
except:
    from urllib.parse import urlencode


class Request(object):
    def __init__(self):
        self.schema = ''
        self.method = ''
        self.host = ''
        self.path = ''
        self.headers = OrderedDict()
        self.query = OrderedDict()
        self.body = ''
        self.form = dict()
        self.connection_timeout = 0
        self.socket_timeout = 0

    def set_shema(self, schema):
        self.schema = schema

    def set_method(self, method):
        self.method = method

    def set_host(self, host):
        self.host = host

    def set_path(self, path):
        self.path = path

    def set_headers(self, headers):
        self.headers = headers

    def set_query(self, query):
        self.query = query

    def set_body(self, body):
        self.body = body

    def set_connection_timeout(self, connection_timeout):
        self.connection_timeout = connection_timeout

    def set_socket_timeout(self, socket_timeout):
        self.socket_timeout = socket_timeout

    def build(self, doseq=0):
        return self.schema + '://' + self.host + self.path + '?' + urlencode(self.query, doseq)
