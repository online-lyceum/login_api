import logging


from db import db_manager
from db.base import get_session

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult

from fastapi import Response

logger = logging.getLogger(__name__)
router = APIRouter(prefix='/api')

