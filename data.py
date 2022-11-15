import base64
import hmac
import struct
import sys
import time

# Work with database and tokens

TOKEN_TIME_ALIVE = 1800  # In seconds


def hotp(key, counter, digits=6, digest='sha1'):
    '''Generate HOTP(token based by counter)'''
    key = base64.b32decode(key.upper() + '=' * ((8 - len(key)) % 8))
    counter = struct.pack('>Q', counter)
    mac = hmac.new(key, counter, digest).digest()
    offset = mac[-1] & 0x0f
    binary = struct.unpack('>L', mac[offset:offset+4])[0] & 0x7fffffff
    return str(binary)[-digits:].zfill(digits)


def totp(key, digits=6, digest='sha1'):
    '''
    Generate TOTP(token based by time
    :param time_step: Time which token is valid
    '''
    return hotp(key, int(time.time() / TOKEN_TIME_ALIVE), digits, digest)


def verify_token(token: str) -> bool:
    # TODO Check if totp for now equal token
    # Maybe pyotp from pypi
    pass


def main():
    args = [int(x) if x.isdigit() else x for x in sys.argv[1:]]
    for key in sys.stdin:
        print(totp(key.strip(), *args))


if __name__ == '__main__':
    main()
