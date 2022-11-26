from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from data import User, Token

routes = APIRouter()


# @routes.post("/")
@routes.get("/")
async def index():
    return "This is login_api for authorise users"


@routes.post("/user/register")
async def create_user(user: User):
    if await User.exist(user.login):
        return Response(status_code=status.HTTP_409_CONFLICT)
    await User.create(login=user.login, password=user.password)
    return Response(status_code=status.HTTP_200_OK)


@routes.get("/user/new_token")
async def new_token(user: User):
    if not await User.exist(user.login):
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    if not User.validate_password(user.login, user.password):
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    token = await Token.generate_token(user.login, user.password)
    return token


@routes.get("/user/validate_token")
async def validate_token(token: Token):
    '''
    :ret: HTTP_404_NOT_FOUND if token not found, HTTP_200_OK if token exist for user
    '''
    if not await Token.validate_token(token.user_login, token.key):
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_200_OK)