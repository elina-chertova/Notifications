from abc import ABC, abstractmethod


class AsyncStorage(ABC):
    @abstractmethod
    async def get(self, query: str):
        pass

    async def update(self, query: str):
        pass
