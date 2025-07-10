# coding:utf-8

from volcengine.viking_db import Index, VikingDBService
from volcengine.viking_db.common import RetryOption


class IndexClient(Index):
    def __init__(self, collection_name, index_name,  host="api-vikingdb.volces.com", region="cn-north-1", ak="", sk="", scheme='http',
                 connection_timeout=30, socket_timeout=30, proxy=None, retry_option=None):
        vikingdb_service = VikingDBService(host, region, ak, sk, scheme, connection_timeout, socket_timeout, proxy, retry_option)
        self.viking_db_service = vikingdb_service
        self.collection_name = collection_name
        self.index_name = index_name
        self.primary_key = "__primary_key"
        self._is_client = True
        self.retry_option = retry_option if retry_option else RetryOption()
