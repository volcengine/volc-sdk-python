from abc import ABC, abstractmethod
from typing import Tuple, List
import json
try:
    import torch
except ImportError:
    raise ImportError("Please make sure to install torch: \n pip install torch~=1.13")

from ..priv_conf import *


class TextPrivatizer(ABC):
    def __init__(self,
                 task_type: Literal["classification", "generation"],
                 priv_conf: "PrivConf") -> None:
        """
        Init
        :param task_type: task type, classification or generation
        :param priv_conf: privacy config
        :return None
        """
        super().__init__()
        self.task_type = task_type
        self.priv_conf = priv_conf

        self.train_data = None
        self.test_data = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    @abstractmethod
    def fit(self,
            train_path: str,
            test_path: Optional[str] = None) -> None:
        """
        Perform text privatization
        :param train_path: input path of training data
        :param test_path: input path of test data
        :return None
        """
        pass

    def load_data(self,
                  train_path: str,
                  test_path: Optional[str] = None) -> None:
        """
        Load training data and test data in jsonl format
        :param train_path: input path of training data
        :param test_path: input path of test data
        :return None
        """
        self.train_data = []
        with open(train_path, "r") as jsonl_file:
            for line in jsonl_file:
                data = json.loads(line.strip())
                self.train_data.append(data)

        if test_path:
            self.test_data = []
            with open(test_path, "r") as jsonl_file:
                for line in jsonl_file:
                    data = json.loads(line.strip())
                    self.test_data.append(data)

    def data_preprocess(self) -> Tuple[List[str], List[str], List[str]]:
        """
        Perform data preprocess
        :return (train_text, train_label, test_text): content of the user (text) and the assistant (label)
        in training data and test data
        """
        train_text, train_label, test_text = [], [], []
        for dic in self.train_data:
            for sub_dic in dic["messages"]:
                if sub_dic["role"] == "user":
                    train_text.append(sub_dic["content"])
                elif sub_dic["role"] == "assistant":
                    train_label.append(sub_dic["content"])
            if len(train_text) != len(train_label):
                raise ValueError("There is a problem with the format of the training data set.")

        if self.test_data:
            for dic in self.test_data:
                for sub_dic in dic["messages"]:
                    if sub_dic["role"] == "user":
                        test_text.append(sub_dic["content"])

        return train_text, train_label, test_text

    def data_postprocess(self, privated_text: List[str]) -> None:
        """
        Perform data postprocess
        :param privated_text: text after privatization
        :return None
        """
        index = 0
        for i in range(len(self.train_data)):
            for sub_dic in self.train_data[i]["messages"]:
                if sub_dic["role"] == "user":
                    sub_dic["content"] = privated_text[index]
                    index += 1

    def save(self,
             out_dir: Optional[str] = None) -> None:
        """
        Save the privatized data
        :param out_dir: output directory
        :return None
        """
        out_dir = "" if out_dir is None else out_dir
        with open(out_dir + "privatized_train_data.jsonl", "w") as jsonl_file:
            for data in self.train_data:
                json_line = json.dumps(data, ensure_ascii=False)
                jsonl_file.write(json_line + "\n")

        if self.test_data:
            with open(out_dir + "privatized_test_data.jsonl", "w") as jsonl_file:
                for data in self.train_data:
                    json_line = json.dumps(data, ensure_ascii=False)
                    jsonl_file.write(json_line + "\n")





