import sys
if sys.version_info < (3, 7):
    raise Exception("为正常使用火山文本隐私化服务，请将您的 Python 版本升级到 3.7 或更高版本！")
from dataclasses import dataclass


@dataclass
class PrivConf:
    pass
