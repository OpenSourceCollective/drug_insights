import os

from dotenv import load_dotenv
from langchain.agents import AgentExecutor, ConversationalChatAgent
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import (
    StreamlitChatMessageHistory,
)
from langchain_openai import AzureChatOpenAI

load_dotenv(".env")


class ChatAndRetrievalExecutor:
    def __init__(self) -> None:
        self.llm = AzureChatOpenAI(
            openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
            azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
        )
        self.tools = []  # TODO: Add tools here
        self.msgs = StreamlitChatMessageHistory()
        self.memory = ConversationBufferMemory(
            chat_memory=self.msgs,
            return_messages=True,
            memory_key="chat_history",
            output_key="output",
        )
        self.chat_agent = ConversationalChatAgent.from_llm_and_tools(
            llm=self.llm, tools=self.tools
        )
        self.executor = AgentExecutor.from_agent_and_tools(
            agent=self.chat_agent,
            tools=self.tools,
            memory=self.memory,
            return_intermediate_steps=True,
            handle_parsing_errors=True,
        )

    def invoke(self, *args, **kwargs):
        return self.executor.invoke(*args, **kwargs)
