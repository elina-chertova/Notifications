import datetime

import src.core.query as sql_query
from src.core.settings import logger, settings
from src.storage.postgres import Postgres


class UserNtfPrep:
    def __init__(self):
        self.sender = settings.service_email
        self.sender_password = settings.service_password
        self.db = Postgres()

    def insert_ntf(self,
                   params: dict) -> dict[str, str]:
        """
        Insert new type of notification to notice table.
        :param params: {column_name: value}
        :return:
        """
        insert_ntf = {
                      'ntf_id': params['id'],
                      'destination': params['destination'],
                      'type': params['message'],
                      'subject': params['subject'],
                      'title': params['title'],
                      'text': params['text'],
                      'content': '',
                      'priority': 'high',
                      'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                      'source': params['source'],
                      'status': 'undone',
                      'created': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                      'modified': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

        ntfs, _ = self.db.get_data(sql_query.check_nft_exists.format(insert_ntf['ntf_id'],
                                                                     insert_ntf['status'], insert_ntf['source']))
        usr, _ = self.db.get_data(sql_query.check_nft_pending.format(insert_ntf['ntf_id']))

        if not usr and not ntfs:
            self.db.insert_update(sql_query.insert_new_notice.format(tuple(insert_ntf.values())))
            logger.info('Inserted data to notification.notice')
        else:
            logger.info('Rows exist in notification.user_ntf or notification.notice and try to send.')
        return insert_ntf

    def download_data(self,
                      query: str) -> None:
        """
        Run generating new notification's type.
        :param query:
        :return:
        """
        _, params = self.db.get_data(query=query)
        for param in params:
            _ = self.insert_ntf(params=param)

    def generate_ntf(self,
                     users_query: str = sql_query.users_A,
                     nft_query: str = sql_query.ntf_undone,
                     update_undone: str = sql_query.update_ntf) -> None:
        """
        Generate new value with users ready to sending.
        :return:
        """
        user, _ = self.db.get_data(query=users_query)
        ntfs, _ = self.db.get_data(query=nft_query)

        us_ntf = ([*us, *ntf, 'pending'] for ntf in ntfs for us in user)
        self.db.insert_many(query=sql_query.insert_us_ntf, data=us_ntf)
        self.db.insert_update(query=update_undone)
        logger.info('Updated data to notification.user_ntf')

    def run(self,
            query: str,
            users_query: str = sql_query.users_A,
            nft_query: str = sql_query.ntf_undone) -> None:
        """
        Generate users' notifications with status 'pending'.
        :param query:
        :param users_query:
        :param nft_query:
        :return:
        """
        self.download_data(query)
        self.generate_ntf(users_query, nft_query)
