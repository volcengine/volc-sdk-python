import logging
import sys


def get_logger(name: str):
    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt="%(asctime)s \t %(levelname)s \t %(name)s \t %(message)s",
                                               datefmt="%Y-%m-%d %H:%M:%S"))
        logger.addHandler(handler)

    return logger


class TLSUtil:
    @staticmethod
    # html空格符处理与前端保持一致
    def replace_white_space_character(origin: str):
        if str is None:
            return None
        else:
            return origin.replace("\r", "\\r").replace("\n", "\\n").replace("\t", "\\t")
