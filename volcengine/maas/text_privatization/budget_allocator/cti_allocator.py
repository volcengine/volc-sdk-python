from typing import Tuple, List
try:
    import numpy as np
    from transformers.tokenization_utils import PreTrainedTokenizer
except ImportError:
    raise ImportError("Please make sure to install numpy and transformers: \n pip install numpy "
                      "\n pip install transformers~=4.30")

from .allocator import BudgetAllocator


class CTIBudgetAllocator(BudgetAllocator):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.budget_dict = {"1": 500, "2": 400, "3": 300}

    def pre_fit(self,
                tokenizer: "PreTrainedTokenizer",
                text: List[str],
                label: List[str]
                ) -> Tuple[np.ndarray, List[int]]:
        """
        Dynamically allocate privacy budget based on the contributing token identification (CTI) method
        :param tokenizer: tokenizer
        :param text: input text of user
        :param label: text label corresponding to the input text
        :return (adaptive_budget, label): adaptive privacy budget corresponding to each token and numeric label
        """
        # Tokenize and convert text labels to numeric types
        input_id = tokenizer(text)["input_ids"]
        label_set = set(label)
        label_dict = {element: index for index, element in enumerate(label_set)}
        label = [label_dict[label] for label in label]

        # Count the frequency of each token in each category
        class_num = len(label_set)
        count = np.zeros((class_num, tokenizer.vocab_size))
        for i in range(len(input_id)):
            for j in range(len(input_id[i])):
                count[label[i]][input_id[i][j]] += 1
        sums = np.sum(count, axis=1)
        freq = np.zeros(count.shape)
        for i in range(len(count)):
            freq[i, :] = count[i, :] / sums[i]

        # Compute the utility importance
        ksi = 1 / max(sums)
        utility_importance = np.zeros(count.shape)
        for i in range(class_num):
            for j in range(tokenizer.vocab_size):
                if count[i][j] > 0:
                    utility_importance[i][j] = sum(
                        [np.log((freq[i][j] / (freq[k][j] + 3 * ksi))) for k in range(class_num) if k != i])

        # Determine privacy budget based on the privacy protection level
        if self.priv_conf.base_budget:
            if self.priv_conf.base_budget > 0:
                base_budget = self.priv_conf.base_budget
            else:
                raise ValueError("The base budget is required to be a positive number.")
        else:
            base_budget = self.budget_dict[self.priv_conf.priv_level]
        adaptive_budget = np.maximum(utility_importance, 0.6) * base_budget

        return adaptive_budget, label
