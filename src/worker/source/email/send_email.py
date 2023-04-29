import smtplib
from abc import abstractmethod
from email.message import EmailMessage

from jinja2 import BaseLoader, Environment, Template

from src.core.query import gen, gen_source, update_usr_nft
from src.core.settings import Settings
from src.storage.postgres import Postgres
from src.worker.source.base import Source
from queue import Queue, Empty
from threading import Thread
import hashlib


class SMTPConnectionPool:
    def __init__(self, server, port, username, password, pool_size=10):
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.pool = Queue(maxsize=pool_size)
        for _ in range(pool_size):
            self.pool.put(smtplib.SMTP_SSL(server, port))

    def get_connection(self):
        try:
            conn = self.pool.get(block=False)
        except Empty:
            conn = smtplib.SMTP_SSL(self.server, self.port)
        conn.login(self.username, self.password)
        return conn

    def return_connection(self, conn):
        self.pool.put(conn)

    def close(self):
        while True:
            try:
                conn = self.pool.get(block=False)
                conn.quit()
            except Empty:
                break


class Email(Source):
    def __init__(self):
        self.config = Settings()
        self.db = Postgres()
        self.sender = self.config.service_email
        self.sender_password = self.config.service_password
        self.smtp_pool = SMTPConnectionPool('smtp.gmail.com', 465, self.sender, self.sender_password)

    def render_template(self, source: str, params: dict, msg_type: str, email: str = ''):
        _, data = self.db.get_data(gen.format(source, msg_type))
        if msg_type == 'welcome':
            verification_link = generate_verification_link(email=email)
            html_code = data[0]['html_code'].format(verification_link, verification_link)
        else:
            html_code = data[0]['html_code']
        template = Environment(loader=BaseLoader()).from_string(html_code)
        result_output = template.render(**params)
        return result_output

    def commit(self, message: dict):
        self.db.insert_update(update_usr_nft.format(message['user_id'], message['ntf_id']))

    def send_email(self, email: str, subject: str, template: Template):
        try:
            conn = self.smtp_pool.get_connection()
            message = EmailMessage()
            message["From"] = self.sender
            message["To"] = ",".join([email])
            message["Subject"] = subject
            message.add_alternative(template, subtype='html')
            conn.send_message(message)
            self.smtp_pool.return_connection(conn)
        except smtplib.SMTPAuthenticationError as e:
            print('\nError email:', e)

    def send(self, email: str, subject: str, template: Template):
        t = Thread(target=self.send_email, args=(email, subject, template))
        t.start()


def generate_verification_link(email):
    hash_object = hashlib.sha256(email.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    verification_link = 'http://0.0.0.0:8012/confirm?email={}&hash={}'.format(email, hex_dig)
    return verification_link
