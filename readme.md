# Сервис нотификаций



## Запуск
`docker-compose -f docker-compose-app.yml up`
#### Шедулер: `python schedule/scheduler.py`
#### Консьюмер: `src/worker/worker.py`


OpenAPI: `http://0.0.0.0:8012/api/openapi`

## Струткура
### Источники уведомлений
1. Панель администратора
2. Генератор автоматических событий
3. API для приема уведомлений

### Используемые таблицы в Postgres
1. email_template

<img src="images/email_template.png" alt="Alt text" title="Optional title" style="display: inline-block; margin: 0 auto; max-width: 100px">


2. notice

<img src="images/notice.png" alt="Alt text" title="Optional title" style="display: inline-block; margin: 0 auto; max-width: 100px">

3. user_ntf

<img src="images/user_ntf.png" alt="Alt text" title="Optional title" style="display: inline-block; margin: 0 auto; max-width: 100px">

4. user

<img src="images/user.png" alt="Alt text" title="Optional title" style="display: inline-block; margin: 0 auto; max-width: 100px">






