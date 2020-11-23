import base64
import json
import sys

from volcengine.vod.VodPlayService import VodPlayService


class VodPlayServiceWrapper(VodPlayService):
    def get_play_auth_token(self, params):
        token = self.get_sign_url('GetPlayInfo', params)
        ret = {'TokenVersion': 'V2', 'GetPlayInfoToken': token}
        data = json.dumps(ret)
        if sys.version_info[0] == 3:
            return base64.b64encode(data.encode('utf-8')).decode('utf-8')
        else:
            return base64.b64encode(data.decode('utf-8'))
