import streamlit as st
from langchain.schema import ChatMessage
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_core.runnables import RunnableConfig

from agents.executors import ChatAndRetrievalExecutor

st.title("🤖 Drug Insights")
st.write(
    """This is a public tool that people can use to for drug safety
1.  To know about drug interactions. Like if you want to take a medication, you can use it to check if it is safe to use it with another medication
2. Use the app to know what side effects the medication may have and what to avoid
This will work by
1. People entering the name of the medication in the app or scanning a barcode
2. ⁠entering the name of 2 drugs and seeing if they are safe to use together."""
)


# define agent executor
agent_executor = ChatAndRetrievalExecutor()

with st.sidebar:
    st.write("Available actions show up here.")

# initialize session state
if len(agent_executor.msgs.messages) == 0 or st.sidebar.button(
    "Reset chat history"
):
    st.session_state["messages"] = [
        ChatMessage(role="assistant", content="How can I help you?")
    ]
    agent_executor.msgs.clear()
    agent_executor.msgs.add_ai_message("How can I help you?")
    st.session_state.steps = {}

avatars = {"human": "user", "ai": "assistant"}
for idx, msg in enumerate(agent_executor.msgs.messages):
    with st.chat_message(avatars[msg.type]):
        # Render intermediate steps if any were saved
        for step in st.session_state.steps.get(str(idx), []):
            if step[0].tool == "_Exception":
                continue
            with st.status(
                f"**{step[0].tool}**: {step[0].tool_input}", state="complete"
            ):
                st.write(step[0].log)
                st.write(step[1])
        st.write(msg.content)


if prompt := st.chat_input():
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(
            st.container(), expand_new_thoughts=True
        )

        cfg = RunnableConfig()
        cfg["callbacks"] = [st_cb]
        response = agent_executor.executor.invoke(prompt, cfg)
        st.write(response["output"])
        st.session_state.steps[str(len(agent_executor.msgs.messages) - 1)] = (
            response["intermediate_steps"]
        )
