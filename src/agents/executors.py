import os

from dotenv import load_dotenv
from langchain.chains import (
    create_history_aware_retriever,
    create_retrieval_chain,
)
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import (
    StreamlitChatMessageHistory,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import AzureChatOpenAI
from vector_db.pinecone import PineconeDB

from .prompts.qa_prompts_2 import CONTEXTUALIZE_Q_SYSTEM_PROMPT, QA_SYSTEM_PROMPT

# from langchain.agents import AgentExecutor, ConversationalChatAgent
# from langchain.chains import ConversationalRetrievalChain
# from langchain_core.messages import HumanMessage
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough

load_dotenv(".env")


class ChatAndRetrievalExecutor:
    def __init__(
        self,
        system_prompt: str = QA_SYSTEM_PROMPT,
        context_prompt: str = CONTEXTUALIZE_Q_SYSTEM_PROMPT,
    ) -> None:
        self.llm = AzureChatOpenAI(
            openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
            azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
        )
        self.msgs = StreamlitChatMessageHistory()
        self.memory = ConversationBufferMemory(
            chat_memory=self.msgs,
            return_messages=True,
            memory_key="chat_history",
            output_key="answer",
        )
        # self.tools = []  # TODO: Add tools here. Tools may not be needed.
        self.retriever = PineconeDB().vectorstore_retriever(
            search_type="mmr", search_kwargs={"k": 3, "fetch_k": 3}
        )
        # self.chat_agent = ConversationalRetrievalChain.from_llm(
        #     llm=self.llm,
        #     # tools=self.tools,
        #     # system_message=system_prompt,
        #     # human_message=user_prompt,
        #     memory=self.memory,
        #     retriever=self.retriever,
        #     verbose=True,
        # )
        # self.executor = AgentExecutor.from_agent_and_tools(
        #     agent=self.chat_agent,
        #     tools=self.tools,
        #     # memory=self.memory,
        #     return_intermediate_steps=True,
        #     handle_parsing_errors=True,
        # )

        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", context_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        history_aware_retriever = create_history_aware_retriever(
            self.llm, self.retriever, contextualize_q_prompt
        )
        question_answer_chain = create_stuff_documents_chain(
            self.llm, qa_prompt
        )
        self.executor = create_retrieval_chain(
            history_aware_retriever, question_answer_chain
        )

        self.history = []

    def invoke(self, *args, **kwargs):
        return self.executor.invoke(*args, **kwargs)

    # def
