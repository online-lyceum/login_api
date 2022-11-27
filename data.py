import base64
from pydantic import BaseModel
import pyotp
import asyncpg

# Work with database and tokens

TOKEN_TIME_ALIVE = 1800  # In seconds

users = []
tokens = {}


class DBHandler:
    def __init__(self):
        self.conn = await asyncpg.connect(host='127.0.0.1', port=5432)
        self.prepare()

    def prepare(self):
        self.conn.execute('''
            CREATE TABLE users(
                id serial PRIMARY KEY,
                login varchar,
                password varchar
            );
            CREATE TABLE tokens(
                id serial PRIMARY KEY,
                user_login varchar,
                key varchar
            );
        ''')

    def add_token(self, user_login: str, token_key: str):
        await self.conn.execute(f'''
            INSERT INTO tokens
            VALUES ($1, $2);
        ''', user_login, token_key)

    def get_tokens(self, user_login: str) -> list:
        '''
        :return: List[str] with token.key for user_login
        '''
        row = await self.conn.fetchrow('SELECT key FROM users WHERE user_login = $1', user_login)
        return list(row)

    def add_user(self, user_login: str, user_password: str):
        await self.conn.execute('''
            INSERT INTO users
            VALUES ($1, $2);
        ''', user_login, user_password)

    def get_user(self, user_login: str):
        row = await self.conn.fetchrow('SELECT * FROM users WHERE login = $1', user_login)
        return User(*row)


database = DBHandler()


class Token(BaseModel):
    key: str
    user_login: str

    @staticmethod
    async def generate_token(user_login: str, user_password: str):
        key = pyotp.TOTP(base64.b32encode(user_password.encode()),
                         12, interval=TOKEN_TIME_ALIVE).now()
        tokens[user_login] = tokens.get(user_login, []) + [key]
        database.add_token(user_login, key)
        return Token(key=key, user_login=user_login)

    @staticmethod
    async def validate_token(user_login: str, token_key: str):
        try:
            psw = [u.password for u in users if u.login == user_login][0]
        except IndexError:
            return False
        psw = base64.b32encode(psw.encode())
        for token in database.get_tokens(user_login):
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
        return True if database.get_user(login) else False

    @staticmethod
    async def create(login: str, password: str):
        users.append(User(login=login, password=password))
        database.add_user(login, password)

    @staticmethod
    async def validate_password(login: str, password: str):
        user = database.get_user(login)
        if user.login == login:
            return user.password == password
        return False
