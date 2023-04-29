import smtplib
from abc import abstractmethod
from email.message import EmailMessage

from jinja2 import BaseLoader, Environment, Template

from src.core.query import gen, gen_source, update_usr_nft
from src.core.settings import Settings
from src.storage.postgres import Postgres
from src.worker.source.base import Source


class Email(Source):
    def __init__(self):
        self.config = Settings()
        self.sender = self.config.service_email
        self.sender_password = self.config.service_password
        self.db = Postgres()

    def render_template(self, source: str, params: dict, msg_type: str):
        if msg_type:
            _, data = self.db.get_data(gen.format(source, msg_type))
        else:
            _, data = self.db.get_data(gen_source.format(source))
        template = Environment(loader=BaseLoader()).from_string(data[0]['html_code'])
        result_output = template.render(**params)
        return result_output

    def commit(self, message: dict):
        self.db.insert_update(update_usr_nft.format(message['user_id'], message['ntf_id']))

    @abstractmethod
    def send(self, email: str, subject: str, template: Template):
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        try:
            server.login(self.sender, self.sender_password)
            message = EmailMessage()
            message["From"] = self.sender
            message["To"] = ",".join([email])
            message["Subject"] = subject
            message.add_alternative(template, subtype='html')
            server.sendmail(self.sender, [email], message.as_string())
        except smtplib.SMTPAuthenticationError as e:
            print('\nError email:', e)
        server.close()


# em = Email()
# service_email = 'evchertova@miem.hse.ru'
# service_password = 'Boss1849'
# subject = 'hell'
# email = 'evchertova@miem.hse.ru'
# template = '<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n</head>\n<body>\n    <div style="width: 630px; font: var(--font-500,600 Suisse,Arial,Helvetica,sans-serif); text-align: center;">\n\t\t<div style="text-align: center;">\n\t\t\t<h1>Best movies</h1>\n\t\t</div>\n\t\t<div style="width: 100%; background: #f0f5f8; border-radius: 10px; margin-top: 10px; padding: 10px;">\n\t\t\t<h2 style="color: #0474ff;">\n\t\t\t\tHello, Элина Чертова!\n\t\t\t</h2>\n\t\t\t<p style="width: 95%; margin: 10px auto; font-size: 18px;">\n\t\t\t\tMovies list: [{\'id\': \'05d7341e-e367-4e2e-acf5-4652a8435f93\', \'title\': \'The Secret World of Jeffree Star\', \'imdb_rating\': 9.5}, {\'id\': \'c241874f-53d3-411a-8894-37c19d8bf010\', \'title\': \'Star Wars SC 38 Reimagined\', \'imdb_rating\': 9.5}, {\'id\': \'c49c1df9-6d06-47b7-87db-d96190901fa4\', \'title\': \'Ringo Rocket Star and His Song for Yuri Gagarin\', \'imdb_rating\': 9.4}, {\'id\': \'0d5e1522-cc03-454b-b501-085348206b81\', \'title\': \'All-Star Party for Carol Burnett\', \'imdb_rating\': 9.2}, {\'id\': \'2e5561a2-bb7f-48d3-8249-fb668db6014a\', \'title\': \'Lunar: The Silver Star\', \'imdb_rating\': 9.2}]\n\t\t\t</p>\n\t\t</div>\n\t\t<div>\n\t\t\t<p style="text-align: center;">\n\t\t\t\t<a href="" style="color: #0474ff; font-size: 12px;">Click here to unsubscribe</a>\n\t\t\t</p>\n\t\t</div>\n\t</div>\n</body>\n</html>'
# em = Email()
# em.send(email, subject, template)

# message = MIMEMultipart()
#         message['From'] = email_data.email_from
#         message['To'] = email_data.email_to
#         message['Subject'] = email_data.subject
#         message.attach(MIMEText(email_data.body, 'plain'))
#
#         # send email
#         with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
#             smtp.ehlo()
#             smtp.starttls()
#             smtp.ehlo()
#             smtp.login('your_email@gmail.com', 'your_password')
#             smtp.sendmail(email_data.email_from, email_data.email_to, message.as_string())




# gmail_user = 'evchertova@miem.hse.ru'
# subject = 'Registration'
# email_type = 'personal'
# params = {'title': 'Registate', 'user': 'Donna Doctor', 'description': 'I am writing something'}
#
# em = Email()
# res = em.extract_template(auto_gen.format('best_movies'))
# em.render_template(res[0])
# print(res)
# em.additional_params(res[0])
# em.form_message(res[0])
# for item in res:
#     message, params, subject, source, html_code = item[1], item[2], item[3], item[4], item[5]
# em.send(gmail_user, subject, email_type, params)
#
