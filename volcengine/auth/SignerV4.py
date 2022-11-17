# coding : utf-8
import datetime
import sys

import pytz

try:
    from urllib import urlencode
except:
    from urllib.parse import urlencode

from volcengine.auth.MetaData import MetaData
from volcengine.util.Util import Util
from volcengine.base.Request import Request
from volcengine.auth.SignResult import SignResult

class SignerV4(object):
    @staticmethod
    def sign(request, credentials):
        if request.path == '':
            request.path = '/'
        if request.method != 'GET' and not ('Content-Type' in request.headers):
            request.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=utf-8'

        format_date = SignerV4.get_current_format_date()
        request.headers['X-Date'] = format_date
        if credentials.session_token != '':
            request.headers['X-Security-Token'] = credentials.session_token

        md = MetaData()
        md.set_algorithm('HMAC-SHA256')
        md.set_service(credentials.service)
        md.set_region(credentials.region)
        md.set_date(format_date[:8])

        hashed_canon_req = SignerV4.hashed_canonical_request_v4(request, md)
        md.set_credential_scope('/'.join([md.date, md.region, md.service, 'request']))

        signing_str = '\n'.join([md.algorithm, format_date, md.credential_scope, hashed_canon_req])
        signing_key = SignerV4.get_signing_secret_key_v4(credentials.sk, md.date, md.region, md.service)
        sign = Util.to_hex(Util.hmac_sha256(signing_key, signing_str))
        request.headers['Authorization'] = SignerV4.build_auth_header_v4(sign, md, credentials)
        return

    @staticmethod
    def sign_url(request, credentials):
        format_date = SignerV4.get_current_format_date()
        date = format_date[:8]

        md = MetaData()
        md.set_date(date)
        md.set_service(credentials.service)
        md.set_region(credentials.region)
        md.set_signed_headers('')
        md.set_algorithm('HMAC-SHA256')
        md.set_credential_scope('/'.join([md.date, md.region, md.service, 'request']))

        query = request.query
        query['X-Date'] = format_date
        query['X-NotSignBody'] = ''
        query['X-Credential'] = credentials.ak + '/' + md.credential_scope
        query['X-Algorithm'] = md.algorithm
        query['X-SignedHeaders'] = md.signed_headers
        query['X-SignedQueries'] = ''
        query['X-SignedQueries'] = ';'.join(sorted(query.keys()))
        if credentials.session_token != '':
            query['X-Security-Token'] = credentials.session_token

        hashed_canon_req = SignerV4.hashed_simple_canonical_request_v4(request, md)
        signing_str = '\n'.join([md.algorithm, format_date, md.credential_scope, hashed_canon_req])
        signing_key = SignerV4.get_signing_secret_key_v4(credentials.sk, md.date, md.region, md.service)
        sign = SignerV4.signature_v4(signing_key, signing_str)

        query['X-Signature'] = sign
        return urlencode(query)

    @staticmethod
    def sign_only(param, credentials):
        request = Request()
        request.host = param.host
        request.method = param.method
        request.path = param.path
        request.body = param.body
        request.query = param.query
        request.headers = param.header_list

        format_date = param.date.strftime("%Y%m%dT%H%M%SZ")
        date = format_date[:8]
        request.headers['X-Date'] = format_date
        md = MetaData()
        md.set_algorithm('HMAC-SHA256')
        md.set_service(credentials.service)
        md.set_region(credentials.region)
        md.set_date(date)
        md.set_credential_scope('/'.join([md.date, md.region, md.service, 'request']))

        if param.is_sign_url:
            md.set_signed_headers('')
            md.set_credential_scope('/'.join([md.date, md.region, md.service, 'request']))
            query = request.query
            query['X-Date'] = format_date
            query['X-NotSignBody'] = ''
            query['X-Credential'] = credentials.ak + '/' + md.credential_scope
            query['X-Algorithm'] = md.algorithm
            query['X-SignedHeaders'] = md.signed_headers
            query['X-SignedQueries'] = ''
            query['X-SignedQueries'] = ';'.join(sorted(query.keys()))
            if credentials.session_token != '':
                query['X-Security-Token'] = credentials.session_token
            hashed_canon_req = SignerV4.hashed_simple_canonical_request_v4(request, md)
        else:
            if credentials.session_token != '':
                request.headers['X-Security-Token'] = credentials.session_token
            hashed_canon_req = SignerV4.hashed_canonical_request_v4(request, md)

        signing_str = '\n'.join([md.algorithm, format_date, md.credential_scope, hashed_canon_req])
        signing_key = SignerV4.get_signing_secret_key_v4(credentials.sk, md.date, md.region, md.service)
        sign = SignerV4.signature_v4(signing_key, signing_str)

        result = SignResult()
        result.xdate = format_date
        result.xAlgorithm = md.algorithm
        if param.is_sign_url:
            result.xSignedQueries = request.query['X-SignedQueries']
        result.xSignedHeaders = md.signed_headers
        result.xCredential = credentials.ak + '/' + md.credential_scope
        result.xSignature = sign
        result.xContextSha256 = request.headers['X-Content-Sha256']
        result.authorization = result.xAlgorithm + " Credential=" + result.xCredential + ", SignedHeaders=" + md.signed_headers + ", Signature=" + result.xSignature
        result.xSecurityToken = credentials.session_token

        return result

    @staticmethod
    def hashed_simple_canonical_request_v4(request, meta):
        body = bytes()
        # if sys.version_info[0] == 3:
        #     body_hash = Util.sha256(body.decode('utf-8'))
        # else:
        body_hash = Util.sha256(body)

        if request.path == '':
            request.path = '/'

        canoncial_request = '\n'.join(
            [request.method, Util.norm_uri(request.path), Util.norm_query(request.query), '\n',
             meta.signed_headers, body_hash])
        # if sys.version_info[0] == 3:
        #     return Util.sha256(canoncial_request.decode('utf-8'))
        # else:
        return Util.sha256(canoncial_request)

    @staticmethod
    def hashed_canonical_request_v4(request, meta):
        # if sys.version_info[0] == 3:
        #     body_hash = Util.sha256(request.body.decode('utf-8'))
        # else:
        body_hash = Util.sha256(request.body)
        request.headers['X-Content-Sha256'] = body_hash

        signed_headers = dict()
        for key in request.headers:
            if key in ['Content-Type', 'Content-Md5', 'Host'] or key.startswith('X-'):
                signed_headers[key.lower()] = request.headers[key]

        if 'host' in signed_headers:
            v = signed_headers['host']
            if v.find(':') != -1:
                split = v.split(':')
                port = split[1]
                if str(port) == '80' or str(port) == '443':
                    signed_headers['host'] = split[0]

        signed_str = ''
        for key in sorted(signed_headers.keys()):
            signed_str += key + ':' + signed_headers[key] + '\n'

        meta.set_signed_headers(';'.join(sorted(signed_headers.keys())))

        canoncial_request = '\n'.join(
            [request.method, Util.norm_uri(request.path), Util.norm_query(request.query), signed_str,
             meta.signed_headers, body_hash])

        return Util.sha256(canoncial_request)

    @staticmethod
    def signature_v4(signing_key, signing_str):
        return Util.to_hex(Util.hmac_sha256(signing_key, signing_str))

    @staticmethod
    def get_signing_secret_key_v4(sk, date, region, service):
        if sys.version_info[0] == 3:
            kdate = Util.hmac_sha256(bytes(sk, encoding='utf-8'), date)
        else:
            kdate = Util.hmac_sha256(sk.encode('utf-8'), date)
        kregion = Util.hmac_sha256(kdate, region)
        kservice = Util.hmac_sha256(kregion, service)
        return Util.hmac_sha256(kservice, 'request')

    @staticmethod
    def build_auth_header_v4(signature, meta, credentials):
        credential = credentials.ak + '/' + meta.credential_scope
        return meta.algorithm + ' Credential=' + credential + ', SignedHeaders=' + meta.signed_headers + ', Signature=' + signature

    @staticmethod
    def get_current_format_date():
        return datetime.datetime.now(tz=pytz.timezone('UTC')).strftime("%Y%m%dT%H%M%SZ")
