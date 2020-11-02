# coding:utf-8
import json


class ComplexEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Statement):
            return {'Effect': o.effect,
                    'Action': o.action,
                    'Resource': o.resource}
        if isinstance(o, InnerToken):
            return {
                'LTAccessKeyId': o.lt_access_key_id,
                'AccessKeyId': o.access_key_id,
                'SignedSecretAccessKey': o.signed_secret_access_key,
                'ExpiredTime': o.expired_time,
                'PolicyString': o.policy_string,
                'Signature': o.signature
            }
        if isinstance(o, Policy):
            return {
                'Statement': [item for item in o.statements]
            }
        return json.JSONEncoder.default(self, o)


class Policy(object):
    def __init__(self, statements):
        self.statements = statements


class Statement(object):
    def __init__(self):
        self.effect = ''
        self.action = []
        self.resource = []
        self.condition = ''

    @staticmethod
    def new_allow_statement(actions, resources):
        s = Statement()
        s.effect = "Allow"
        s.action = actions
        s.resource = resources
        return s

    @staticmethod
    def new_deny_statement(actions, resources):
        s = Statement()
        s.effect = "Deny"
        s.action = actions
        s.resource = resources
        return s


class SecurityToken2(object):
    def __init__(self):
        self.access_key_id = ''
        self.secret_access_key = ''
        self.session_token = ''
        self.expired_time = ''
        self.current_time = ''

    def __str__(self):
        return json.dumps({
            'AccessKeyId': self.access_key_id,
            'SecretAccessKey': self.secret_access_key,
            'SessionToken': self.session_token,
            'ExpiredTime': self.expired_time,
            'CurrentTime': self.current_time
        })


class InnerToken(object):
    def __init__(self):
        self.lt_access_key_id = ''
        self.access_key_id = ''
        self.signed_secret_access_key = ''
        self.expired_time = 0
        self.policy_string = ''
        self.signature = ''

    def __str__(self):
        return json.dumps({
            'LTAccessKeyId': self.lt_access_key_id,
            'AccessKeyId': self.access_key_id,
            'SignedSecretAccessKey': self.signed_secret_access_key,
            'ExpiredTime': self.expired_time,
            'PolicyString': self.policy_string,
            'Signature': self.signature
        })
