from typing import Optional, List
import os
import math
import random
try:
    import numpy as np
    import torch
    from transformers import AutoTokenizer
    from transformers.tokenization_utils import PreTrainedTokenizer
except ImportError:
    raise ImportError("Please make sure to install numpy, torch, and transformers: \n pip install numpy "
                      "\n pip install torch~=1.13 \n pip install transformers~=4.30")

from .privatizer import TextPrivatizer
from ..budget_allocator import CTIBudgetAllocator


class TextClsPrivatizer(TextPrivatizer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.tokenizer = None
        self.embedding_model = None
        self.budget_allocator = CTIBudgetAllocator(self.priv_conf)

    def load_tokenizer_embedding(self,
                                 tokenizer: "PreTrainedTokenizer",
                                 embedding_model: "torch.nn.Embedding") -> None:
        """
        Load the tokenizer and embedding model
        :param tokenizer: tokenizer
        :param embedding_model: embedding model
        :return None
        """
        self.tokenizer = tokenizer
        self.embedding_model = embedding_model.to(self.device)

    def privatize(self,
                  text: List[str],
                  label: List[int],
                  adaptive_budget: np.ndarray) -> List[str]:
        """
        Privatize the text in batches
        :param text: original text to be privatized
        :param label: label corresponding to the original text
        :param adaptive_budget: adaptive budget
        :return privated_text: text after privatization
        """
        # Privatize in batches
        batch_size = 32
        batch_num = math.ceil(len(text) / batch_size)
        privated_ids = []
        for i in range(batch_num):
            sub_text = text[i * batch_size: (i + 1) * batch_size]
            sub_label = label[i * batch_size: (i + 1) * batch_size]
            model_input = self.tokenizer(sub_text, padding="longest", return_tensors="pt")
            input_ids, mask = model_input["input_ids"].to(self.device), model_input["attention_mask"].to(self.device)
            # add noise to embedding vector
            input_embeds = self.embedding_model(input_ids)
            shape = input_embeds.shape
            input_embeds = input_embeds.view(-1, shape[2])
            ones_count_per_row = mask.sum(dim=1)
            mask = mask.view(-1, 1)
            repeated_labels = np.repeat(sub_label, shape[1])
            mvn = torch.distributions.MultivariateNormal(torch.zeros(shape[2]).to(self.device),
                                                         covariance_matrix=torch.eye(shape[2]).to(self.device))
            vec = mvn.sample((len(input_embeds),))
            vec = torch.nn.functional.normalize(vec, p=2, dim=1)
            l = [
                random.gammavariate(alpha=shape[2], beta=1 / adaptive_budget[repeated_labels[j]][input_ids.view(-1)[j]])
                for j in range(len(input_embeds))]
            input_embeds = input_embeds + vec * (torch.tensor(l).view(-1, 1).to(self.device) * mask).to(torch.float32)
            # find nearest embedding vector
            nearest_indices = torch.argmin(torch.cdist(input_embeds, self.embedding_model.weight.data.to(torch.float32),
                                                       p=2), dim=1).view(shape[0], shape[1])
            result = [row[shape[1] - j + 2:].tolist() for row, j in zip(nearest_indices, ones_count_per_row)]
            privated_ids = privated_ids + result

        privated_text = self.tokenizer.batch_decode(privated_ids)

        return privated_text

    def fit(self,
            train_path: str,
            test_path: Optional[str] = None) -> None:
        """
        Perform text privatization
        :param train_path: input path of training data
        :param test_path: input path of test data
        :return None
        """
        self.load_data(train_path, test_path)

        # Perform data preprocess and determine privacy budget
        train_text, train_label, test_text = self.data_preprocess()
        adaptive_budget, train_label = self.budget_allocator.pre_fit(self.tokenizer, train_text, train_label)

        # Privatize and postprocess
        privated_train_text = self.privatize(train_text, train_label, adaptive_budget)
        self.data_postprocess(privated_train_text)
        if self.test_data:
            privated_test_text = self.privatize(test_text, [0] * len(test_text), np.max(adaptive_budget, axis=0))
            self.data_postprocess(privated_test_text)

        del self.tokenizer
        del self.embedding_model
