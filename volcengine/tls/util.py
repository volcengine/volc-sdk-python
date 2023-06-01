class TLSUtil:
    @staticmethod
    # html空格符处理与前端保持一致
    def replace_white_space_character(origin: str):
        if str is None:
            return None
        else:
            return origin.replace("\r", "\\r").replace("\n", "\\n").replace("\t", "\\t")
