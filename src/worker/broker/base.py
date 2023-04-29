from abc import abstractmethod


class BaseQueue:
    @abstractmethod
    def produce(self, *args, **kwargs):
        pass

    @abstractmethod
    def consume(self, *args, **kwargs):
        pass
