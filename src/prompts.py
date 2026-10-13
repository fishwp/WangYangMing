import yaml
from src.config import PROMPT_FILE


def _load():
    with open(PROMPT_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f)


_data = _load()

SYSTEM_PROMPT = _data["system_prompt"]
MODEL_NAME = _data["model"]["name"]
TEMPERATURE = _data["model"]["temperature"]
MAX_TOKENS = _data["model"]["max_tokens"]
RETRY_MAX = _data["retry"]["max_attempts"]
RETRY_WAIT = _data["retry"]["wait_seconds"]
