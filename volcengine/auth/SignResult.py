# coding:utf-8

class SignResult(object):
    def __init__(self):
        self.xdate = ''
        self.xCredential = ''
        self.xAlgorithm = ''
        self.xSignedHeaders = ''
        self.xSignedQueries = ''
        self.xSignature = ''
        self.xContextSha256 = ''
        self.xSecurityToken = ''

        self.authorization = ''

    def __str__(self):
        return '\n'.join(['%s:%s' % item for item in self.__dict__.items()])
