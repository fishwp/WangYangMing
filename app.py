import streamlit as st
from src.agent import stream_agent_reply
from src.prompts import SYSTEM_PROMPT

st.set_page_config(page_title="知行陪伴者", page_icon="🧭")
st.title("知行陪伴者")
st.caption("帮你看清知与行之间那道缝隙，一次只走一步。")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
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
            for delta in stream_agent_reply(st.session_state.messages):
                full += delta
                placeholder.write(full)
        except Exception as e:
            placeholder.error(f"出错了：{e}")
            full = "（本次回复失败，请检查网络或 API 配置）"

    st.session_state.messages.append({"role": "assistant", "content": full})