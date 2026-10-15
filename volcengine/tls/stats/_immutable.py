# coding=utf-8
"""Internal base for write-once public health snapshot objects."""
from __future__ import absolute_import


class _ImmutableSnapshot(object):
    """Allow each slot to be initialized once, then reject mutation/deletion."""

    __slots__ = ()

    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise AttributeError(
                "{} is immutable".format(self.__class__.__name__))
        object.__setattr__(self, name, value)

    def __delattr__(self, name):
        raise AttributeError(
            "{} is immutable".format(self.__class__.__name__))
