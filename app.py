import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

st.title("王阳明行动陪伴智能体（第 1 周 Demo）")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你是王阳明风格的行动陪伴助手，用简洁、务实、知行合一的方式回应。"}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if prompt := st.chat_input("说说你此刻的困惑或想做的事…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full = ""
        stream = client.chat.completions.create(
            model="deepseek-chat",
            messages=st.session_state.messages,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            full += delta
            placeholder.write(full)

    st.session_state.messages.append({"role": "assistant", "content": full})