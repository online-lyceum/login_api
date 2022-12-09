import base64
import pyotp
import asyncio
from pydantic import BaseModel
from fastapi import Depends

#import aiosqlite

# Work with database and tokens

TOKEN_TIME_ALIVE = 1800  # In seconds
TokenDB, UserDB = None, None


class DBHandler:
    def __init__(self):
        self._tokens = {}
        self._users = []

    async def add_token(self, user_id: str, token_key: str):
        self._tokens[user_id] = self._tokens.get(user_id, []) + [token_key]

    async def get_tokens(self, user_id: str) -> list | None:
        '''return None if user_id not exist else List[str]'''
        return self._tokens.get(user_id, None)

    async def add_user(self, login: str, password: str):
        self._users.append((login, password))

    async def get_user(self, login: str) -> 'User':
        for user_login, user_psw in self._users:
            if user_login == login:
                return User(login=user_login, password=user_psw)


#class DBHandler:
#    def __init__(self):
#        #self.cursor = self.db.cursor()
#        #self.session = Depends(get_session)
#        self.prepare()
#
#    async def prepare(self):
#        db = aiosqlite.connect('data.db')
#        await db.__aenter__()
#        await db.execute('''
#            CREATE TABLE users(
#                id INTEGER PRIMARY KEY,
#                login varchar UNIQUE,
#                password varchar
#            );
#            ''')
#        await db.execute('''
#            CREATE TABLE tokens(
#                id INTEGER PRIMARY KEY,
#                user_login varchar,
#                key varchar
#            );
#        ''')
#        await db.commit()
#        await db.close()

#    async def add_token(self, user_login: str, token_key: str):
        #new_token = TokenDB(user_login=user_login, key=token_key)
#        db = aiosqlite.connect('data.db')
#        await db.__aenter__()
#        await db.execute(f"INSERT INTO tokens(user_login, key) VALUES ('{user_login}', '{token_key}')")
#        await db.commit()
#        #session.add(new_token)
#        #return new_token
#        
#    async def get_tokens(self, user_login: str) -> list:
#        '''
#        :return: List[str] with token.key for user_login
#        '''
#        ret = []
#        db = aiosqlite.connect('data.db')
#        await db.__aenter__()
#        async with db.execute(f"SELECT key FROM tokens WHERE user_login='{user_login}'") as cursor:
#            for row in cursor:
#                ret.append(row)
#        return ret

#    async def add_user(self, user_login: str, user_password: str):
        #new_user = UserDB(login=user_login, password=user_password)
#        db = aiosqlite.connect('data.db')
#        await db.__aenter__()
#        await db.execute(f"INSERT INTO users(login, password) VALUES ('{user_login}', '{user_password}')")
#        await db.commit()

#    async def get_user(self, user_login: str):
#        db = aiosqlite.connect('data.db')
#        await db.__aenter__()
#        cursor = await db.execute(f"SELECT * FROM users WHERE login='{user_login}'")
#        u = await cursor.fetchone()
#        login, password = u[1:]
#        return User(login=login, password=password)


database = DBHandler()


class Token(BaseModel):
    key: str
    user_login: str

    @staticmethod
    async def generate_token(user_login: str, user_password: str):
        key = pyotp.TOTP(base64.b32encode(user_password.encode()),
                         12, interval=TOKEN_TIME_ALIVE).now()
        #tokens[user_login] = tokens.get(user_login, []) + [key]
        token = await database.add_token(user_login, key)
        return Token(key=key, user_login=user_login)

    @staticmethod
    async def validate_token(user_login: str, token_key: str):                              
        psw = await database.get_user(user_login)
        psw = psw.password
        psw = base64.b32encode(psw.encode())
        for token in await database.get_tokens(user_login):
            if token == token_key:
                if not pyotp.TOTP(psw, 12, interval=TOKEN_TIME_ALIVE).verify(token, valid_window=2):
                    #tokens[user_login].remove(token)
                    return False
                return True
        return False


class User(BaseModel):
    login: str
    password: str

    @staticmethod
    async def exist(login: str):
        return True if await database.get_user(login) else False

    @staticmethod
    async def create(login: str, password: str) -> 'User':
        await database.add_user(login, password)
        return User(login=login, password=password)

    @staticmethod
    async def validate_password(login: str, password: str):
        user = await database.get_user(login)
        if user.login == login:
            return user.password == password
        return False


async def main():
    ulist = [('a', '123'), ('b', '321'), ('c', '555')]
    for login, psw in ulist:
        await User.create(login, psw)
        print(login, 'created')
    for login, _ in ulist:
        print(login, await User.exist(login))
    tokens = []
    for login, psw in ulist:
        t = await Token.generate_token(login, psw)
        tokens.append(t)
    print(tokens)


if __name__ == '__main__':
    #asyncio.run(init_models())
    asyncio.run(main())
