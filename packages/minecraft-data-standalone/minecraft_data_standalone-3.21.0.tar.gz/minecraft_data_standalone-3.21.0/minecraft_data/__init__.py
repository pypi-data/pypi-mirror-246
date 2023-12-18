from os import path
import sys

from minecraft_data.tools import convert, commondata


class mod(sys.modules[__name__].__class__):
    data_folder: str
    def __call__(self, version, edition = 'pc'):
        return type(version, (object,), convert(self.data_folder, version, edition))

    def common(self, edition = 'pc'):
        return type('common', (object,), commondata(self.data_folder, edition))


sys.modules[__name__].__class__ = mod
