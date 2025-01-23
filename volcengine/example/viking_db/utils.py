from volcengine.viking_db import VikingDBService
import os

def get_vikingdb_service():
    ak = os.getenv("ak")
    sk = os.getenv("sk")
    host = "api-vikingdb.volces.com"
    region = "cn-beijing"
    scheme = "http"
    connection_timeout = 30
    socket_timeout = 30

    vikingdb_service = VikingDBService(
        host=host, region=region, scheme=scheme,
        connection_timeout=connection_timeout, socket_timeout=socket_timeout
    )
    vikingdb_service.set_ak(ak)
    vikingdb_service.set_sk(sk)
    return vikingdb_service