import json
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

from src.vector_db.pinecone import PineconeDB

from .prompts.qa_prompts import CONTEXTUALIZE_Q_SYSTEM_PROMPT, QA_SYSTEM_PROMPT

load_dotenv(".env")

with open("config.json", "r") as f:
    config = json.load(f)

CONTEXTUALIZE_Q_SYSTEM_PROMPT = config.get(
    "contextualize_q_system_prompt", CONTEXTUALIZE_Q_SYSTEM_PROMPT
)
QA_SYSTEM_PROMPT = config.get("qa_system_prompt", QA_SYSTEM_PROMPT)
VECTOR_DB_THRESHOLD = config.get("vector_db_threshold", 0.9)


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
        self.retriever = PineconeDB().vectorstore_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"score_threshold": VECTOR_DB_THRESHOLD},
        )

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
