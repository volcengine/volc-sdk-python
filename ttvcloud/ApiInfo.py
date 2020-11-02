# coding:utf-8


class ApiInfo(object):
    def __init__(self, method, path, query, form, header):
        self.method = method
        self.path = path
        self.query = query
        self.form = form
        self.header = header

    def __str__(self):
        return 'method: ' + self.method + ', path: ' + self.path
