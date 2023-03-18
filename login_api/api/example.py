import logging

from fastapi import APIRouter, Depends

import schemas
from services.user import UserService


logger = logging.getLogger(__name__)
router = APIRouter(
    prefix='/api',
    tags=["Hello"],
)


@router.get('')
async def register_user(user: schemas.user.User,
						service: Depends(UserService)):
    return 'Hello from FastAPI and Lawrence'
