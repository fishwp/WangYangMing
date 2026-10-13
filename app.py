# 启动方式：D:\Anaconda\envs\wangyangming\python.exe -m streamlit run app.py
import streamlit as st
from src.llm import chat, plan, LLMError
from src.prompts import SYSTEM_PROMPT
from src.schemas import Plan

st.set_page_config(page_title="知行陪伴者", page_icon="🧭")
st.title("知行陪伴者")
st.caption("帮你看清知与行之间那道缝隙，一次只走一步。")

mode = st.sidebar.radio("模式", ["对话", "生成计划"])


if mode == "对话":
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    if user_input := st.chat_input("说说你此刻卡住的事…"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            try:
                reply = chat(st.session_state.messages)
                st.write(reply)
            except LLMError as e:
                reply = "（本次回复失败，请检查网络或 API 配置）"
                st.error(f"出错了：{e}")

        st.session_state.messages.append({"role": "assistant", "content": reply})

else:
    situation = st.text_area("描述你现在的困境", height=160)
    if st.button("生成计划") and situation.strip():
        with st.spinner("正在生成…"):
            try:
                p: Plan = plan(situation)
                st.subheader("反思")
                st.write(p.reflection.situation)
                st.write("**阻碍：** " + p.reflection.obstacle)
                st.write("**洞察：** " + p.reflection.insight)

                st.subheader("立志")
                st.write("**目标：** " + p.aspiration.goal)
                st.write("**为什么：** " + p.aspiration.why)
                st.write("**标准：** " + p.aspiration.standard)

                st.subheader("行动")
                st.write("**第一步：** " + p.action.first_step)
                st.write(f"**时长：** {p.action.duration_minutes} 分钟")
                st.write("**阻力应对：** " + p.action.obstacle_plan)

                st.subheader("复盘")
                if p.review:
                    st.write("**已完成：** " + p.review.done)
                    st.write("**差距：** " + p.review.gap)
                    st.write("**下一步：** " + p.review.next_action)
                else:
                    st.info("还没做，等你完成后回来复盘。")
            except LLMError as e:
                st.error(f"生成失败：{e}")
