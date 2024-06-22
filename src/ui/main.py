import streamlit as st

from agents.setup import get_agent
from langchain_community.callbacks import StreamlitCallbackHandler

if "enable_search" not in st.session_state:
    st.session_state["enable_search"] = {}

LIBRARY = ["chat"]

agent = get_agent()
subject = "chat"

st.title("🤖 Drug Insights")
st.write(
    """This is a public tool that people can use to for drug safety
1.  To know about drug interactions. Like if you want to take a medication, you can use it to check if it is safe to use it with another medication
2. Use the app to know what side effects the medication may have and what to avoid
This will work by
1. People entering the name of the medication in the app or scanning a barcode
2. ⁠entering the name of 2 drugs and seeing if they are safe to use together."""
)

if "messages" not in st.session_state:
    st.session_state["messages"] = {
        subject: [
            {
                "role": "assistant",
                "content": f"Hi, You can ask me any question about the {subject}. What would you like to learn about?",
            }
        ]
        for subject in LIBRARY
    }
if (
    not st.session_state.get("agents", False)
    or subject not in st.session_state["agents"]
):
    st.session_state["agents"] = {subject: agent}

for msg in st.session_state.messages[subject]:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not st.session_state.enable_search.get(subject, False):
        st.session_state.enable_search[subject] = False

    st.session_state.messages[subject].append(
        {"role": "user", "content": prompt}
    )
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = st.session_state["agents"][subject].run(
            input=prompt,
            callbacks=[st_callback],
        )
        st.session_state.messages[subject].append(
            {"role": "assistant", "content": response}
        )
        st.write(response)
