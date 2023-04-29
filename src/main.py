"""Script to run FastAPI Notification service."""

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import notifications, subscribe
from db import postgresdb
from src.core.settings import settings

PROJECT_NAME = 'Notification Service'

app = FastAPI(
    title=PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    description='Notification service.',
    version='1.0.0',
)


@app.on_event('startup')
async def startup():
    """Start databases."""
    postgresdb.postgresdb = await postgresdb.get_postgres()


@app.on_event('shutdown')
async def shutdown():
    await postgresdb.postgresdb.close()

app.include_router(subscribe.router, prefix='/api/v1/subscribes', tags=['Subscribe'])
app.include_router(notifications.router, prefix='/api/v1/notifications', tags=['Notifications'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8012,
    )



