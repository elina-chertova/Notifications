import logging
from http import HTTPStatus
from src.models.subscribes import Success
from fastapi import APIRouter, Depends, Query, Request

from src.services.notifications import Notifier, get_notifier_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('/notification/send',
             summary="Send notification from part of service")
async def send_notification(request: Request,
                            type_: str = Query('', description="Message type. Ex. welcome"),
                            user_id: str = Query(None, description="User ID"),
                            subject: str = Query('Notification', description="Message subject"),
                            title: str = Query(None, description="Message title"),
                            text: str = Query(None, description="Message text"),
                            content: str = Query(None, description="Message content. Ex. movie_id"),
                            destination: str = Query('Email', description="Choose type: Email/Websocket"),
                            ntf: Notifier = Depends(get_notifier_service)):
    headers = request.headers.get('X-Request-Id')
    await ntf.send(user_id, subject, title, text, content, destination, headers, type_=type_)
    return Success(message='Done', code=HTTPStatus.OK)
