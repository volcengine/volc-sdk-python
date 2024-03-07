import copy
import json

from volcengine.maas._response import BinaryResponseContent
from volcengine.maas.v2._resource import SyncAPIResource
from volcengine.maas.v2 import MaasService
from volcengine.maas.exception import MaasException, new_client_sdk_request_error
from volcengine.auth.SignerV4 import SignerV4
from volcengine.maas.utils import json_to_object


class Speech(SyncAPIResource):

    def create(self, endpoint_id, req):
        try:
            if not ("audio.speech" in self._service.api_info):
                raise new_client_sdk_request_error(
                    "no such api", req.get("req_id", None)
                )
            api_info = copy.deepcopy(self._service.api_info["audio.speech"])
            api_info.path = api_info.path.format(endpoint_id=endpoint_id)
            r = self._service.prepare_request(api_info, {})
            r.headers["Content-Type"] = "application/json"
            r.body = json.dumps(req)

            SignerV4.sign(r, self._service.service_info.credentials)

            url = r.build()
            res = self._service.session.post(
                url,
                headers=r.headers,
                data=r.body,
                timeout=(
                    self._service.service_info.connection_timeout,
                    self._service.service_info.socket_timeout,
                ),
                stream=True,
            )

            log_id = res.headers.get("x-tt-logid", None)
            if res.status_code != 200:
                raw = res.text.encode()
                res.close()
                try:
                    resp = json_to_object(str(raw, encoding="utf-8"), log_id=log_id)
                except Exception:
                    raise new_client_sdk_request_error(raw, log_id)
                else:
                    if resp.error:
                        raise MaasException(
                            resp.error.code_n,
                            resp.error.code,
                            resp.error.message,
                            log_id,
                        )
                    else:
                        raise new_client_sdk_request_error(resp, log_id)

            return BinaryResponseContent(res, log_id)
        except MaasException:
            raise
        except Exception as e:
            raise new_client_sdk_request_error(str(e))
