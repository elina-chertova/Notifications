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
    rabbit_host = Field(host, env='RABBIT_HOST')
    rabbit_port = Field(5672, env='RABBIT_PORT')
    rabbit_login = Field('guest', env='RABBIT_LOGIN')
    rabbit_pswd = Field('guest', env='RABBIT_PASSWORD')

    service_email = Field('evchertova@miem.hse.ru', env='RABBIT_PASSWORD')
    service_password = Field('Boss1849', env='RABBIT_PASSWORD')

    load_url = {'best_movies': 'films/?sort=imdb_rating%3Adesc&page[size]=5&page[number]=2'}
    # service_host =
    # service_port =

    movie_service_host = Field('127.0.0.1', env='MOVIE_SERVICE_HOST')
    movie_service_port = Field('8005', env="MOVIE_SERVICE_PORT")
    #
    auth_service_host = Field('127.0.0.1', env='AUTH_SERVICE_HOST')
    auth_service_port = Field('5000', env="AUTH_SERVICE_PORT")
    #
    # kafka_host: str = Field('localhost', env="KAFKA_HOST")
    # kafka_port: str = Field('9092', env="KAFKA_PORT")
    #
    # clickhouse_host: str = Field('localhost', env="CLICKHOUSE_HOST")
    # clickhouse_port: str = Field('9000', env="CLICKHOUSE_PORT")
    #
    # service_host: str = Field('localhost', env='SERVICE_HOST')
    #
    # mongodb_host: str = Field('localhost', env='MONGODB_HOST')
    # mongodb_port: str = Field('27017', env='MONGODB_PORT')
    # app_port: int = 8003


settings = Settings()
rabbit_settings = RabbitMQSettings()
psgr_settings = PostgresSettings()
