import streamlit as st
from ustndquery.example import astream_run
import asyncio
st.title("Hello World")
pr = None
if "messages" not in st.session_state:
    st.session_state.messages = []
chat = st.container()
chat.chat_message("assistant").write("Hello")

if pr:=st.chat_input("Your message"):
    print(pr)
    for i in st.session_state.messages:
        print(f"i={i}")
        chat.chat_message(i["role"]).write(i["content"])
    chat.chat_message("assistant").write(f"Echo: {pr}")
    st.session_state.messages.append({"role": "user", "content": pr})
    res = astream_run(pr)
    full_response = ""
    message_placeholder = st.empty()
    st.session_state.messages.append(message_placeholder)
    async def _run(res,full_response = ""):
        async for r in res:
            full_response +=f"{r}"
            message_placeholder.write({"role": "AI", "content": full_response})
            st.session_state.messages[-1] = message_placeholder
        st.session_state.messages[-1] = {"role": "AI", "content": full_response}

    d1 = asyncio.run(_run(res))

