from typing import Protocol

from langchain.agents.agent import AgentExecutor


class Agent(Protocol):
    def initialize(self) -> AgentExecutor:
        pass
