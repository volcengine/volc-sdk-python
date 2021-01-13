import base64
import json
import sys

from google.protobuf.json_format import MessageToJson

from volcengine.models.vod.request.request_vod_pb2 import VodGetPlayInfoRequest
from volcengine.vod.VodPlayService import VodPlayService


class VodPlayServiceWrapper(VodPlayService):

    def get_play_auth_token(self, request: VodGetPlayInfoRequest):
        try:
            jsonData = MessageToJson(request, False, True)
            params = json.loads(jsonData)
            for k, v in params.items():
                if isinstance(v, (int, float, bool, str)) is True:
                    continue
                else:
                    params[k] = json.dumps(v)
            token = self.get_sign_url('GetPlayInfo', params)
            ret = {'TokenVersion': 'V2', 'GetPlayInfoToken': token}
            data = json.dumps(ret)
        except Exception as Argument:
            raise Argument
        else:
            if sys.version_info[0] == 3:
                return base64.b64encode(data.encode('utf-8')).decode('utf-8')
            else:
                return base64.b64encode(data.decode('utf-8'))

