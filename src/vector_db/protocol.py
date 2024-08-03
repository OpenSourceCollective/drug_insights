from typing import Any, List, Protocol


class VectorDB(Protocol):
    def _create_index(self, *args, **kwarg) -> None:
        pass

    def insert(self, *args, **kwarg) -> None:
        pass

    def vectorstore_search(self, query: str, k: int = 3) -> List[Any]:
        pass

    def vectorstore_retriever(self) -> Any:
        pass

    def delete_index(self, name: str) -> None:
        pass
