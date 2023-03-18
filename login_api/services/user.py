import logging

from sqlalchemy import select
from fastapi import status, HTTPException

from .base import BaseService
import schemas
from db import tables


logger = logging.getLogger(__name__)


class UserService(BaseService):
    async def get(
            self, *,
            user_id: int
    ) -> tables.User:
        query = select(tables.User)

        if user_id is not None:
            query = query.filter_by(
                user_id=user_id
            )

        user = await self.session.scalar(query)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return user

    async def create(
            self,
            user_schema: schemas.user.User
    ):
        new_user = tables.User(**user_schema.dict())
        self.session.add(new_teacher)
        await self.session.commit()
        return new_teacher

    async def delete(
            self,
            user_id: int
    ):
        user = await self.get(user_id=user_id)
        await self.session.delete(user)
        await self.session.commit()
