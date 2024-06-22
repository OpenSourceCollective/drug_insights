import os

from langchain.agents import AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain_openai import AzureChatOpenAI


def get_agent():
    llm = AzureChatOpenAI(
        openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
    )
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        azure_deployment="35-turbo-dev",
    )

    tools = []  # TODO: Add tools here

    return initialize_agent(
        tools,
        llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        handle_parsing_errors=True,
        max_iterations=5,
        verbose=True,
        # return_intermediate_steps=True,
    )
