import os
from typing import Tuple

try:
    import torch
    from transformers import AutoModel, AutoTokenizer
    from transformers.tokenization_utils import PreTrainedTokenizer
except ImportError:
    raise ImportError("Please make sure to install torch and transformers: "
                      "\n pip install torch~=1.13 \n pip install transformers~=4.30.2")


def get_bottom_model(model_id: str) -> Tuple["PreTrainedTokenizer", "torch.nn.Embedding"]:
    """
    Load the specified pre-trained model from huggingface and save the embedding model and tokenizer
    :param model_id: id of pre-trained model
    :return None
    """
    model = AutoModel.from_pretrained(model_id, trust_remote_code=True)

    # Search the embedding layer
    for name, module in model.named_modules():
        if isinstance(module, torch.nn.Embedding):
            break

    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)

    return tokenizer, module
