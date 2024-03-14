
from volcengine.maas.v2._resource import SyncAPIResource
from volcengine.maas.v2.audio.speech import Speech


class Audio(SyncAPIResource):
    __speech: Speech = None

    @property
    def speech(self) -> Speech:
        if self.__speech is None:
            self.__speech = Speech(self._service)
        return self.__speech
