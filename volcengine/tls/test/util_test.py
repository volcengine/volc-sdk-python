# coding=utf-8
import os

from volcengine.tls.TLSService import TLSService

def NewTLSService():
    return TLSService(
        endpoint=os.environ["VOLCENGINE_ENDPOINT"],
        access_key_id=os.environ["VOLCENGINE_ACCESS_KEY_ID"],
        access_key_secret=os.environ["VOLCENGINE_ACCESS_KEY_SECRET"],
        region=os.environ["VOLCENGINE_REGION"],
    )

