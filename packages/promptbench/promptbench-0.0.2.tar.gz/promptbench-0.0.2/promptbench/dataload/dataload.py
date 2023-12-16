# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from .dataset import *

SUPPORTED_DATASETS = [
    "sst2", "cola", "qqp",
    "mnli", "mnli_matched", "mnli_mismatched",
    "qnli", "wnli", "rte", "mrpc",
    "mmlu", "squad_v2", "un_multi", "iwslt2017", "math",
    "bool_logic", "valid_parentheses",
    "gsm8k", "csqa", "bigbench_date", "bigbench_object_tracking",
    'last_letter_concat', 'numersense', 'qasc'
]

class DatasetLoader:
    
    @staticmethod
    def load_dataset(dataset_name, supported_languages=None):
        """
        Load and return the specified dataset.

        This function acts as a factory method, returning the appropriate dataset object 
        based on the provided dataset name. Note that 'un_multi' and 'iwslt' require 
        additional arguments to specify the languages used in the dataset.

        The supported languages are: 
            - 'de': 'German',
            - 'en': 'English',
            - 'fr': 'French',

        Args:
            dataset_name (str): The name of the dataset to load.
            supported_languages: list: Additional arguments required by 'iwslt'. 
                                Please visit https://huggingface.co/datasets/iwslt2017 to see the supported languages for iwslt.
                                e.g. supported_languages=['de-en', 'ar-en'] for German-English and Arabic-English translation.
        Returns:
            Dataset object corresponding to the given dataset_name.

        Raises:
            NotImplementedError: If the dataset_name does not correspond to any known dataset.
        """        
        # GLUE datasets
        if dataset_name in ["cola", "sst2", "qqp", "mnli", "mnli_matched", "mnli_mismatched", 
                            "qnli", "wnli", "rte", "mrpc"]:
            return GLUE(dataset_name)
        elif dataset_name == 'mmlu':
            return MMLU()
        elif dataset_name == "squad_v2":
            return SQUAD_V2()
        elif dataset_name == 'un_multi':
            return UnMulti()
        elif dataset_name == 'iwslt2017':
            return IWSLT(supported_languages)
        elif dataset_name == 'math':
            return Math()
        elif dataset_name == 'bool_logic':
            return BoolLogic()
        elif dataset_name == 'valid_parentheses':
            return ValidParentheses()
        elif dataset_name == 'gsm8k':
            return GSM8K()
        elif dataset_name == 'csqa':
            return CSQA()
        elif 'bigbench' in dataset_name:
            return BigBench(dataset_name)
        else:
            # If the dataset name doesn't match any known datasets, raise an error
            raise NotImplementedError(f"Dataset '{dataset_name}' is not supported.")

