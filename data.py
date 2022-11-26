import base64
from pydantic import BaseModel
import pyotp

# Work with database and tokens

TOKEN_TIME_ALIVE = 1800  # In seconds

users = []
tokens = {}


class Token(BaseModel):
    key: str
    user_login: str

    @staticmethod
    async def generate_token(user_login: str, user_password: str):
        key = pyotp.TOTP(base64.b32encode(user_password.encode()),
                         12, interval=TOKEN_TIME_ALIVE).now()
        tokens[user_login] = tokens.get(user_login, []) + [key]
        return Token(key=key, user_login=user_login)

    @staticmethod
    async def validate_token(user_login: str, token_key: str):
        try:
            psw = [u.password for u in users if u.login == user_login][0]
        except IndexError:
            return False
        psw = base64.b32encode(psw.encode())
        for token in tokens.get(user_login, []):
            if token == token_key:
                if not pyotp.TOTP(psw, 12, interval=TOKEN_TIME_ALIVE).verify(token, valid_window=2):
                    tokens[user_login].remove(token)
                    return False
                return True
        return False


class User(BaseModel):
    login: str
    password: str

    @staticmethod
    async def exist(login: str):
        for u in users:
            if u.login == login:
                return True
        return False

    @staticmethod
    async def create(login: str, password: str):
        users.append(User(login=login, password=password))

    @staticmethod
    async def validate_password(login: str, password: str):
        for user in users:
            if user.login == login:
                return user.password == password
        return False