from abc import abstractmethod


class Source:
    @abstractmethod
    async def send(self, *args, **kwargs):
        pass

    async def render_template(self, *args, **kwargs):
        pass

    async def commit(self, *args, **kwargs):
        pass

    async def send_email(self, *args, **kwargs):
        pass
