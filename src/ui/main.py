import streamlit as st
from agents.executors import ChatAndRetrievalExecutor
from agents.handlers import PrintRetrievalHandler, StreamHandler
from agents.helpers import get_by_session_id
from langchain.schema import ChatMessage
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.runnables.history import RunnableWithMessageHistory

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
        # for step in st.session_state.steps.get(str(idx), []):
        #     if step[0].tool == "_Exception":
        #         continue
        #     with st.status(
        #         f"**{step[0].tool}**: {step[0].tool_input}", state="complete"
        #     ):
        #         st.write(step[0].log)
        #         st.write(step[1])
        st.write(msg.content)


if query := st.chat_input():
    st.chat_message("user").write(query)
    # st.session_state.messages.append(
    #     {"role": "user", "content": query}
    # )
    agent_executor.msgs.add_user_message(query)

    with st.chat_message("assistant"):
        # TODO: fix handlers to show context and retrieval
        # retrieval_handler = PrintRetrievalHandler(st.container())
        # stream_handler = StreamHandler(st.empty())
        # response = agent_executor.chat_agent.run(
        #     query, callbacks=[retrieval_handler, stream_handler]
        # )
        # st.write(response)

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

        # st_cb = StreamlitCallbackHandler(
        #     st.container(), expand_new_thoughts=True
        # )
        # cfg = RunnableConfig()
        # cfg["callbacks"] = [st_cb]
        # response = agent_executor.executor.invoke(
        #     {"input": query, "chat_history": agent_executor.history},
        #     config=cfg,
        # )
        # agent_executor.history.extend(
        #     [HumanMessage(content=query), response["answer"]]
        # )

        st.write(response["answer"])
        # st.write(response)
        # st.write(response["output"])
        # st.session_state.steps[str(len(agent_executor.msgs.messages) - 1)] = (
        #     response
        # )
    st.chat_message("assistant").write(response["context"])
    agent_executor.msgs.add_ai_message(response["answer"])
