
from functools import cached_property


from volcengine.maas.v2._resource import SyncAPIResource
from volcengine.maas.v2.audio.speech import Speech


class Audio(SyncAPIResource):
    @cached_property
    def speech(self) -> Speech:
        return Speech(self._service)



