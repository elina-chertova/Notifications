import psycopg2.extras

from src.storage.postgres import Postgres

users = [('11f47c49-9cf8-4ccb-bdcd-e302cd870af6', 'user1',
          '$pbkdf2-sha256$29000$6/3fu3euFaL0fo9xDkEo5Q$Y6oYWeOorzO5QfiBhybbJCCaxG/UWZNLh5HDbdnwJBg', 'user1@mail.ru',
          'Do', 'John', 'f', 't', 'f', '', 'false', '2023-01-14 12:32:43.089274'),
         ('12f47c49-9cf8-4ccb-bdcd-e302cd870af6', 'user2',
          '$pbkdf2-sha256$29000$6/3fu3euFaL0fo9xDkEo5Q$Y6oYWeOo3zO5QfiBhybbJCCaxG/UWZNLh5HDbdnwJBg', 'user2@mail.ru',
          'Bakket', 'Kate', 'f', 't', 'f', '', 'false', '2023-01-14 13:32:43.089274'),
         ('13f47c49-9cf8-4ccb-bdcd-e302cd870af6', 'user3',
          '$pbkdf2-sha256$29000$6/3fu3euFaL0fo9xDkEo5Q$Y6oYWeOo2zO5QfiBhybbJCCaxG/UWZNLh5HDbdnwJBg', 'user3@mail.ru',
          'Cuper', 'Sheldon', 'f', 't', 'f', '', 'false', '2023-01-14 14:32:43.089274'),
         ('14f47c49-9cf8-4ccb-bdcd-e302cd870af6', 'user4',
          '$pbkdf2-sha256$29000$6/3fu3euFaL0fo9xDkEo5Q$Y6oYWeOo6zO5QfiBhybbJCCaxG/UWZNLh5HDbdnwJBg', 'user4@mail.ru',
          'Surel', 'William', 'f', 't', 'f', '', 'false', '2023-01-14 15:32:43.089274')]

users_subscribe = [('11f47c49-9cf8-4ccb-bdcd-e302cd870af6', 'John', 'Do', 'user1@mail.ru', 'A'),
                   ('12f47c49-9cf8-4ccb-bdcd-e302cd870af6', 'Kate', 'Bakket', 'user2@mail.ru', 'A'),
                   ('13f47c49-9cf8-4ccb-bdcd-e302cd870af6', 'Sheldon', 'Cuper', 'user3@mail.ru', 'A'),
                   ('14f47c49-9cf8-4ccb-bdcd-e302cd870af6', 'William', 'Surel', 'user4@mail.ru', 'A')]

insert_users = "INSERT INTO public.user (id, login, password, email, last_name, first_name, " \
               "is_staff, is_active, is_superuser, last_login, subscription, register_date) " \
               "VALUES %s ON CONFLICT DO NOTHING;"
insert_subscriber = "INSERT INTO notification.users (user_id, first_name, last_name, email,  " \
                    "subscribe) VALUES %s ON CONFLICT DO NOTHING;"


def insert_data(fake_users: list[tuple], query: str):
    postgres = Postgres()
    connection = postgres.postgres_connection()
    with connection.cursor() as curs:
        psycopg2.extras.execute_values(curs, query, fake_users)
    connection.commit()


insert_data(users, insert_users)
insert_data(users_subscribe, insert_subscriber)
