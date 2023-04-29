from abc import abstractmethod


class Source:
    @abstractmethod
    async def send(self, **kwargs):
        pass
