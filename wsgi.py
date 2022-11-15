from typing import Union

# Accept and handle data from network


def register_user(username: str, password: str):
    '''Write username and password to database(data module)
    '''
    # TODO Check if username doesnt exist. If exist, send 409 error
    # If not exist, write data to database and send 202 status
    pass


def generate_token(username: str, password: str):
    '''
    :param username: Would be as id for token
    :param password: Would be as secret key for token
    '''
    # TODO Check username existing and validate password. If username not exist, send 404 error
    # If password is not valid, send 403 or 401 or 400 error(?)
    # TODO Generate TOTP(data module), write it to DB and send back
    pass


def validate_token(username: str, token: Union[str, int]):
    '''
    '''
    # TODO Check if token in database(username as key)
    # Send true or false
    pass
