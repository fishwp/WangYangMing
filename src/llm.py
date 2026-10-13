import json
from loguru import logger
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

from src.config import API_KEY, BASE_URL, LOG_DIR
from src.prompts import MODEL_NAME, TEMPERATURE, MAX_TOKENS, RETRY_MAX, RETRY_WAIT
from src.schemas import Plan

logger.add(LOG_DIR / "app.log", rotation="1 MB", encoding="utf-8", enqueue=True)

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


class LLMError(Exception):
    pass


@retry(
    stop=stop_after_attempt(RETRY_MAX),
    wait=wait_fixed(RETRY_WAIT),
    retry=retry_if_exception_type(Exception),
    reraise=True,
)
def _call(messages, response_format=None):
    logger.info("call model={} messages={}", MODEL_NAME, len(messages))
    kwargs = dict(model=MODEL_NAME, messages=messages, temperature=TEMPERATURE, max_tokens=MAX_TOKENS)
    if response_format:
        kwargs["response_format"] = response_format
    return client.chat.completions.create(**kwargs)


def chat(messages):
    try:
        resp = _call(messages)
        return resp.choices[0].message.content
    except Exception as e:
        logger.exception("chat failed")
        raise LLMError(str(e)) from e


def plan(situation: str) -> Plan:
    schema = json.dumps(Plan.model_json_schema(), ensure_ascii=False)
    system = (
        "你是一个行动陪伴智能体的结构化输出模块。"
        "请严格按下面的 JSON Schema 输出，只输出 JSON，不要任何解释或 markdown 代码块。"
        "所有必填字段都必须出现。\n\nSchema:\n" + schema
    )
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": situation},
    ]
    try:
        resp = _call(messages, response_format={"type": "json_object"})
        raw = resp.choices[0].message.content
        logger.debug("raw plan: {}", raw[:300])
        return Plan.model_validate_json(raw)
    except Exception as e:
        logger.exception("plan failed")
        raise LLMError(str(e)) from e
