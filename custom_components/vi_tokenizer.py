import re
from typing import Any, Dict, List, Text
from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.shared.nlu.training_data.message import Message

from rasa.nlu.constants import TOKENS_NAMES, MESSAGE_ATTRIBUTES
from underthesea import word_tokenize

class VietnameseTokenizer(Tokenizer):
    language_list = ["vi"]
    defaults = {
        # Flag to check whether to split intents
        "intent_tokenization_flag": False,
        # Symbol on which intent should be split
        "intent_split_symbol": "_",
        # Text will be tokenized with case sensitive as default
        "case_sensitive": True,
    }

    def __init__(self, component_config: Dict[Text, Any] = None) -> None:
        """Construct a new tokenizer using the TextBlobTokenizer framework."""
        super().__init__(component_config)
        self.case_sensitive = self.component_config["case_sensitive"]

    @classmethod
    def required_packages(cls) -> List[Text]:
        return ["underthesea"]

    def tokenize(self, message: Message, attribute: Text) -> List[Token]:
        text = message.get(attribute)
        words = word_tokenize(text)
        message.set("original_words", text)
        return self._convert_words_to_tokens(words, text)