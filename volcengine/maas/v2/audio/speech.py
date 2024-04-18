import copy
import json

from volcengine.maas._response import BinaryResponseContent
from volcengine.maas.v2._resource import SyncAPIResource
from volcengine.maas.v2 import MaasService
from volcengine.maas.exception import MaasException, new_client_sdk_request_error
from volcengine.auth.SignerV4 import SignerV4
from volcengine.maas.utils import json_to_object
from volcengine.maas.v2.utils import gen_req_id


class Speech(SyncAPIResource):

    def create(self, endpoint_id, req):
        api = "audio.speech"
        req_id = gen_req_id()
        self._service._validate(api, req_id)
        apikey = self._service._setted_apikey

        try:
            res = self._service._call(endpoint_id, api, req_id, {}, json.dumps(req), apikey, stream=True)
            return BinaryResponseContent(res, req_id)
        except MaasException as e:
            raise e
        except Exception as e:
            raise new_client_sdk_request_error(str(e), req_id)
