# login_api

## Run
Need __uvicorn__ for run. For install: ``pip install uvicorn``

``uvicorn main:app --host 0.0.0.0 --port [PORT]``

## Content
``/user/register`` Register a user. In data accept {login: str, password: str}
``/user/new_token`` Generate new token for user. In data accept {login: str, password: str}
``/user/validate_token`` Check if token is exist in database. In data accept {user_login: str, key: str}
