from typing import Optional

import src.core.query as sql_query
from generator.models.event import Event
from src.core.settings import logger
from src.storage.postgres import Postgres
from src.worker.source.email.send_email import Email


class FormMSG:
    def __init__(self):
        self.db = Postgres()
        self.email = Email()

    def get_users(self,
                  source_: str,
                  msg_type: str = '') -> list[dict]:
        """
        Get list of users with some message type to send notifications.
        :param source_:
        :param msg_type:
        :return:
        """
        fields = None
        if source_ == 'Auto':
            _, fields = self.db.get_data(sql_query.pending.format(source_, msg_type))
        elif source_ == 'Admin':
            _, fields = self.db.get_data(sql_query.pending_admin)
        else:
            logger.error('Unexpected message source')
        return fields

    def get_tmpl_params(self,
                        content: Optional[list[str]] | str,
                        field: dict) -> dict[str, str]:
        """
        Form template params.
        :param content:
        :param field:
        :return:
        """
        user = field['first_name'] + ' ' + field['last_name']
        params = {
            'user': user,
            'title': field['title'],
            'text': field['text'],
            'content': content
        }
        return params

    def append_event(self, events: list[Event], field, params):
        template = self.email.render_template(source=field['source'], params=params, msg_type=field['type'])
        events.append(Event(user_id=field['user_id'],
                            ntf_id=field['ntf_id'],
                            msg_type=field['type'],
                            email=field['email'],
                            subject=field['subject'],
                            destination=field['destination'],
                            template=template))
        return events
