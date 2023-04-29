import logging
import os

from pydantic import BaseSettings, Field

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(filename="scheduler.log", level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger('log')

PROJECT_NAME = os.getenv('FasterAPI', 'Notification Service')
host = '127.0.0.1'


class PostgresSettings(BaseSettings):
    user = Field('app', env='PSG_HOST')
    password = Field('123qwe', env='PSG_HOST')
    database = Field('movies_db', env='PSG_HOST')
    host = Field('127.0.0.1', env='PSG_HOST')
    port = Field('5432', env='PSG_HOST')


class RabbitMQSettings(BaseSettings):
    rabbit_host = Field(host, env='RABBIT_HOST')
    rabbit_port = Field(5672, env='RABBIT_PORT')
    rabbit_login = Field('guest', env='RABBIT_LOGIN')
    rabbit_pswd = Field('guest', env='RABBIT_PASSWORD')

    routing_key_email = 'email.{0}.{1}'  # email.admin.best_movies
    queue_email = 'email_queue'
    exchange = 'exchange_email'


class Settings(BaseSettings):
    service_email = Field('evchertova@miem.hse.ru', env='RABBIT_PASSWORD')
    service_password = Field('Boss1849', env='RABBIT_PASSWORD')

    load_url = {'best_movies': 'films/?sort=imdb_rating%3Adesc&page[size]=5&page[number]=1'}

    movie_service_host = Field('127.0.0.1', env='MOVIE_SERVICE_HOST')
    movie_service_port = Field('8005', env="MOVIE_SERVICE_PORT")

    auth_service_host = Field('127.0.0.1', env='AUTH_SERVICE_HOST')
    auth_service_port = Field('5000', env="AUTH_SERVICE_PORT")


settings = Settings()
rabbit_settings = RabbitMQSettings()
psgr_settings = PostgresSettings()
