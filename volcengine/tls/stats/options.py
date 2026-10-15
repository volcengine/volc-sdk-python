"""Explicit, immutable local snapshot query options."""
from volcengine.tls.stats._immutable import _ImmutableSnapshot


class StatsOptions(_ImmutableSnapshot):
    __slots__ = ("_view",)

    def __init__(self, view):
        if view not in ("health", "operational", "debug"):
            raise ValueError("view must be health, operational or debug")
        self._view = view

    @property
    def view(self):
        return self._view

    def __repr__(self):
        return "StatsOptions(view={!r})".format(self.view)
