import streamlit as st
from langchain.schema import ChatMessage
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.runnables.history import RunnableWithMessageHistory

from agents.executors import ChatAndRetrievalExecutor
from agents.helpers import STORE, get_by_session_id

from extractors import parser

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
    agent_executor = ChatAndRetrievalExecutor()
    agent_executor.msgs.clear()
    agent_executor.history = []
    agent_executor.msgs.add_ai_message("How can I help you?")
    st.session_state.steps = {}
    for key in STORE:
        in_memory_history = STORE[key]
        in_memory_history.clear()

avatars = {"human": "user", "ai": "assistant"}
for idx, msg in enumerate(agent_executor.msgs.messages):
    with st.chat_message(avatars[msg.type]):

        st.write(msg.content)


if query := st.chat_input():
    st.chat_message("user").write(query)
    agent_executor.msgs.add_user_message(query)

    with st.chat_message("assistant"):

        st_cb = StreamlitCallbackHandler(
            st.container(), expand_new_thoughts=True
        )
        cfg = RunnableConfig()
        cfg["callbacks"] = [st_cb]
        cfg["configurable"] = {"session_id": "abc123"}
        runner = RunnableWithMessageHistory(
            agent_executor.executor,
            get_by_session_id,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )
        response = runner.invoke(
            {
                "input": query,
            },
            config=cfg,
        )
        agent_executor.history.extend(
            [HumanMessage(content=query), response["answer"]]
        )

        st.write(response["answer"])

    context_list = response["context"]

    parsed_docs = parser.parse_sources_list(context_list)
    if any(parsed_docs):
        with st.expander("See sources"):
            formatted_output = parser.format_parsed_sources(parsed_docs)
            st.markdown(formatted_output)

    agent_executor.msgs.add_ai_message(response["answer"])
