from abc import ABC, abstractmethod
from typing import List
try:
    import torch
    from transformers.tokenization_utils import PreTrainedTokenizer
except ImportError:
    raise ImportError("Please make sure to install torch and transformers: \n pip install torch~=1.13"
                      "\n pip install transformers~=4.30")

from ..priv_conf import *


class BudgetAllocator(ABC):
    def __init__(self,
                 priv_conf: "PrivConf") -> None:
        """
        Init
        :param priv_conf: privacy config
        :return None
        """
        super().__init__()
        self.priv_conf = priv_conf

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    @abstractmethod
    def pre_fit(self,
                tokenizer: "PreTrainedTokenizer",
                text: List[str],
                label: List[str]
                ) -> None:
        """
        Dynamically allocate privacy budget
        :param tokenizer: tokenizer
        :param text: input text of user
        :param label: text label corresponding to the input text
        :return None
        """
        pass
