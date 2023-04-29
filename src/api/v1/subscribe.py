from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request

from src.api.check_data import check_auth
from src.models.subscribes import Success
from src.services.subscribe import Subscribe, get_subscribe_service

router = APIRouter()


@router.post('/subscribe',
             summary="Subscribe",
             response_description="If Done - user has been subscribed",
             description="")
async def subscribe(request: Request,
                    subscriber: Subscribe = Depends(get_subscribe_service),) -> Success:
    user, user_code = await check_auth.get_user(request)

    if user_code == HTTPStatus.OK:
        await subscriber.subscribe(user)
        return Success(message='Done', code=HTTPStatus.OK)
    raise HTTPException(status_code=user_code, detail=user)


@router.post('/unsubscribe',
             summary="Unsubscribe",
             response_description="If Done - user has been unsubscribed",
             description="")
async def unsubscribe(request: Request,
                      subscriber: Subscribe = Depends(get_subscribe_service),) -> Success:
    user, user_code = await check_auth.get_user(request)

    if user_code == HTTPStatus.OK:
        await subscriber.unsubscribe(user)
        return Success(message='Done', code=HTTPStatus.OK)
    raise HTTPException(status_code=user_code, detail=user)


