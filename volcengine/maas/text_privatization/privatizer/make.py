from ..priv_conf import *
from .privatizer import TextPrivatizer
from .cls_privatizer import TextClsPrivatizer


def make(task_type: Literal["classification", "generation"],
         priv_conf: "PrivConf") -> "TextPrivatizer":
    """
    Make an instance
    :param task_type: task type, classification or generation
    :param priv_conf: privacy config
    :return TextPrivatizer
    """
    if isinstance(priv_conf, ClsPrivConf):
        return TextClsPrivatizer(
            task_type,
            priv_conf
        )

    else:
        raise TypeError("unsupported priv_conf type: {}".format(type(priv_conf)))
