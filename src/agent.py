from openai import OpenAI
from src.config import API_KEY, BASE_URL, MODEL_NAME
from src.prompts import SYSTEM_PROMPT

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


def get_agent_reply(messages):
    """接收完整消息列表，返回模型回复文本。"""
    resp = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.7,
        max_tokens=800,
    )
    return resp.choices[0].message.content


def stream_agent_reply(messages):
    """流式版本，逐段 yield 文本。"""
    stream = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.7,
        max_tokens=800,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content or ""
        if delta:
            yield delta
