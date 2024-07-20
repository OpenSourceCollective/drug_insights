from typing import Any, List


class Pinecone:
    def create_index(self, *args, **kwarg) -> None:
        pass

    def insert(self, *args, **kwarg) -> None:
        pass

    def vectorstore_search(self, query: str, k: int = 3) -> List[Any]:
        pass

    def vectorstore_retriever(self) -> Any:
        pass

    def delete_index(self, name: str) -> None:
        pass
