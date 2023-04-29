from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from src.api.check_data import check_auth
from src.models.subscribes import Success
from src.services.subscribe import Subscribe, get_subscribe_service

router = APIRouter()


@router.post('/subscribe',
             summary="",
             response_description="",
             description="")
async def subscribe(request: Request,
                    subscriber: Subscribe = Depends(get_subscribe_service),) -> Success:
    """
    """
    # user, user_code = await check_auth.get_user(request)

    user_code = 200
    user = '11f47c49-9cf8-4ccb-bdcd-e302cd870af6'

    if user_code == HTTPStatus.OK:
        await subscriber.subscribe(user)
        return Success(message='Done', code=HTTPStatus.OK)
    return Success(message='Done', code=200)


@router.post('/unsubscribe',
             summary="",
             response_description="",
             description="")
async def unsubscribe(request: Request,
                      subscriber: Subscribe = Depends(get_subscribe_service),) -> Success:
    """
    """
    # user, user_code = await check_auth.get_user(request)

    user_code = 200
    user = '11f47c49-9cf8-4ccb-bdcd-e302cd870af6'

    if user_code == HTTPStatus.OK:
        await subscriber.unsubscribe(user)
        return Success(message='Done', code=HTTPStatus.OK)
    return Success(message='Done', code=200)


