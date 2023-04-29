"""Script to run FastAPI UGC service."""
# import sentry_sdk
import asyncio

import asyncpg
import uvicorn
# clickhouse, kafka, mongodb
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

# from aiokafka import AIOKafkaProducer
from api.v1 import subscribe, notifications
# from asynch import connect
# from core.config import Settings
# from core.logger import LOGGING
from db import postgresdb
from storage.postgres import PostgresDB

# from motor.motor_asyncio import AsyncIOMotorClient
# from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
# from sentry_sdk.integrations.fastapi import FastApiIntegration

# sentry_sdk.init(integrations=[FastApiIntegration()])
#
# conf = Settings()

PROJECT_NAME = 'Notification Service'

app = FastAPI(
    title=PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    description='Notification service.',
    version='1.0.0',
)
# app.add_middleware(SentryAsgiMiddleware)


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
        # log_config=LOGGING
    )



