import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

load_dotenv()

BASE_DIR = Path(__file__).parent
PROMPT_PATH = BASE_DIR / "agent" / "prompt.md"

def load_system_prompt() -> str:
    if PROMPT_PATH.exists():
        return PROMPT_PATH.read_text(encoding="utf-8")
    return "你是王阳明风格的行动陪伴助手，简洁、务实、知行合一，每次最多问一个问题。"

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

st.set_page_config(page_title="知行陪伴者", page_icon="🧭")
st.title("知行陪伴者")
st.caption("帮你看清知与行之间那道缝隙，一次只走一步。")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": load_system_prompt()}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if prompt := st.chat_input("说说你此刻卡住的事…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full = ""
        try:
            stream = client.chat.completions.create(
                model="deepseek-chat",
                messages=st.session_state.messages,
                stream=True,
                temperature=0.7,
                max_tokens=800,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                full += delta
                placeholder.write(full)
        except Exception as e:
            placeholder.error(f"出错了：{e}")
            full = "（本次回复失败，请检查网络或 API 配置）"

    st.session_state.messages.append({"role": "assistant", "content": full})