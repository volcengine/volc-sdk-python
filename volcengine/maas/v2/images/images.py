import json

from volcengine.maas.exception import new_client_sdk_request_error, MaasException
from volcengine.maas.utils import json_to_object
from volcengine.maas.v2._resource import SyncAPIResource


class Images(SyncAPIResource):

    def quick_gen(self, endpoint_id, req):
        log_id = ""
        try:
            res, log_id = self._service.json_request(
                "images.quick_gen", endpoint_id, {}, json.dumps(req)
            )
            if res == "":
                raise new_client_sdk_request_error("empty response", log_id)
            resp = json_to_object(res, log_id=log_id)
        except MaasException as e:
            raise e
        except Exception as e:
            raise new_client_sdk_request_error(str(e), log_id)
        else:
            return resp
