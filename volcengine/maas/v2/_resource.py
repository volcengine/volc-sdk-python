from volcengine.maas.v2 import MaasService


class SyncAPIResource:
    _service: MaasService

    def __init__(self, service: MaasService) -> None:
        self._service = service
