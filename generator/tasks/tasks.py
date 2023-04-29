from http import HTTPStatus
from typing import Optional

from generator.models.event import Event
from schedule.form import FormMSG
from src.core.settings import logger, settings
from src.core.utils import make_request


class Tasks(FormMSG):
    def __init__(self):
        super().__init__()

    async def best_movies_task(self) -> Optional[list[Event]]:
        fields = self.get_users('Auto', 'best_movies')
        movies_events = []
        for field in fields:
            movies, code = await make_request(host=settings.movie_service_host,
                                              port=settings.movie_service_port,
                                              path=settings.load_url[field['type']])
            if code != HTTPStatus.OK:
                print("Can't get movies' list. Error: {0}".format(code))
                logger.info("Can't get movies' list. Error: {0}".format(code))
                return None
            params = self.get_tmpl_params(content=movies, field=field)
            movies_events = self.append_event(events=movies_events, field=field, params=params)
        return movies_events


