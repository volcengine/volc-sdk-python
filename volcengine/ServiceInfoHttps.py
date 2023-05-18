# coding: utf-8


class ServiceInfoSms(object):
    def __init__(self, host, header, credentials, connection_timeout, socket_timeout, scheme='https'):
        self.host = host
        self.header = header
        self.credentials = credentials
        self.connection_timeout = connection_timeout
        self.socket_timeout = socket_timeout
        self.scheme = scheme
