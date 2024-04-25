import json

from volcengine.maas.exception import new_client_sdk_request_error, MaasException
from volcengine.maas.utils import json_to_object
from volcengine.maas.v2._resource import SyncAPIResource


class Images(SyncAPIResource):

    def quick_gen(self, endpoint_id, req):
        return self._service._request(endpoint_id, "images.quick_gen", req)

    def flex_gen(self, endpoint_id, req):
        return self._service._request(endpoint_id, "images.flex_gen", req)
