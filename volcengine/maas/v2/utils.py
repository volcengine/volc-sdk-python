from datetime import datetime
import random


def gen_req_id():
    return datetime.now().strftime("%Y%m%d%H%M%S") + format(
        random.randint(0, 2**64 - 1), "020X"
    )
