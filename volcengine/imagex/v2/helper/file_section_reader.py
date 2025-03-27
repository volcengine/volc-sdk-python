# coding:utf-8
import os


class FileSectionReader(object):
    def __init__(self, file_object, size, init_offset=None, can_reset=False):
        self.file_object = file_object
        self.size = size
        self.offset = 0
        self.init_offset = init_offset
        self.can_reset = can_reset
        if init_offset:
            self.file_object.seek(init_offset, os.SEEK_SET)

    def read(self, amt=None):
        if self.offset >= self.size:
            return ''

        if (amt is None or amt < 0) or (amt + self.offset >= self.size):
            data = self.file_object.read(self.size - self.offset)
            self.offset = self.size
            return data

        self.offset += amt
        return self.file_object.read(amt)

    @property
    def len(self):
        return self.size

    def reset(self):
        if self.can_reset:
            self.offset = 0
            if self.init_offset is not None:
                self.file_object.seek(self.init_offset, os.SEEK_SET)
