# coding:utf-8
import base64
import hashlib
import hmac
import random
import sys
import uuid
from functools import reduce

from Crypto.Cipher import AES

from volcengine.const.Const import LETTER_RUNES
from zlib import crc32

try:
    from urllib import quote
except:
    from urllib.parse import quote


class Util(object):
    @staticmethod
    def norm_uri(path):
        return quote(path).replace('%2F', '/').replace('+', '%20')

    @staticmethod
    def norm_query(params):
        query = ''
        for key in sorted(params.keys()):
            if type(params[key]) == list:
                for k in params[key]:
                    query = query + quote(key, safe='-_.~') + '=' + quote(k, safe='-_.~') + '&'
            else:
                query = query + quote(key, safe='-_.~') + '=' + quote(params[key], safe='-_.~') + '&'
        query = query[:-1]
        return query.replace('+', '%20')

    @staticmethod
    def hmac_sha256(key, content):
        # type(key) == <class 'bytes'>
        if sys.version_info[0] == 3:
            return hmac.new(key, bytes(content, encoding='utf-8'), hashlib.sha256).digest()
        else:
            return hmac.new(key, bytes(content.encode('utf-8')), hashlib.sha256).digest()

    @staticmethod
    def hmac_sha1(key, content):
        # type(key) == <class 'bytes'>
        if sys.version_info[0] == 3:
            return hmac.new(key, bytes(content, encoding='utf-8'), hashlib.sha1).digest()
        else:
            return hmac.new(key, bytes(content.encode('utf-8')), hashlib.sha1).digest()

    @staticmethod
    def sha256(content):
        # type(content) == <class 'str'>
        if sys.version_info[0] == 3:
            if isinstance(content, str) is True:
                return hashlib.sha256(content.encode('utf-8')).hexdigest()
            else:
                return hashlib.sha256(content).hexdigest()
        else:
            if isinstance(content, (str, unicode)) is True:
                return hashlib.sha256(content.encode('utf-8')).hexdigest()
            else:
                return hashlib.sha256(content).hexdigest()

    @staticmethod
    def to_hex(content):
        lst = []
        for ch in content:
            if sys.version_info[0] == 3:
                hv = hex(ch).replace('0x', '')
            else:
                hv = hex(ord(ch)).replace('0x', '')
            if len(hv) == 1:
                hv = '0' + hv
            lst.append(hv)
        return reduce(lambda x, y: x + y, lst)

    @staticmethod
    def pad(plain_text):
        block_size = AES.block_size

        number_of_bytes_to_pad = block_size - len(plain_text) % block_size
        ascii_string = chr(0)
        padding_str = number_of_bytes_to_pad * ascii_string
        padded_plain_text = plain_text + padding_str
        return padded_plain_text

    @staticmethod
    def generate_access_key_id(prefix):
        uid = str(uuid.uuid4())
        uid_base64 = base64.b64encode(uid.replace('-', '').encode(encoding='utf-8'))

        s = uid_base64.decode().replace('=', '').replace('/', '').replace('+', '').replace('-', '')
        return prefix + s

    @staticmethod
    def rand_string_runes(length):
        return ''.join(random.sample(list(LETTER_RUNES), length))

    @staticmethod
    def aes_encrypt_cbc_with_base64(orig_data, key):
        # type(orig_data) == <class 'str'>
        # type(key) == <class 'bytes'>
        generator = AES.new(key, AES.MODE_CBC, key)
        if sys.version_info[0] == 3:
            crypt = generator.encrypt(Util.pad(orig_data).encode('utf-8'))
            return base64.b64encode(crypt).decode()
        else:
            crypt = generator.encrypt(Util.pad(orig_data))
            return base64.b64encode(crypt)

    @staticmethod
    def generate_secret_key():
        rand_str = Util.rand_string_runes(32)
        return Util.aes_encrypt_cbc_with_base64(rand_str, 'bytedance-isgood'.encode('utf-8'))

    @staticmethod
    def crc32(file_path):
        prev = 0
        for eachLine in open(file_path, "rb"):
            prev = crc32(eachLine, prev)
        return prev & 0xFFFFFFFF
