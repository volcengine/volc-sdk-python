import json
from typing import Any, Dict, Generator
class RespIter:
    def __init__(self, generator: Generator[Dict[str, Any], None, None]):
        self.generator = generator
        self.usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 0}}

    def __iter__(self):
        return self._wrapped_generator()

    def _wrapped_generator(self):
        for part in self.generator:
            usage =part.get("usage")
            if not (usage == "" or  usage == None):
                self.usage = json.loads(usage)
            yield part['generated_answer']

    def token_usage(self):
        return self.usage
