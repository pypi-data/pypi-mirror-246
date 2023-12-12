import os

from pebbleauthclient.constants import JWKS_EXP_TIME
from pebbleauthclient import auth

while True:
    print("Input a valid JWT token (type Q to exit) : ")
    token = input()

    if token.lower() == "q":
        break

    auth_token = auth(token)
    user = auth_token.get_user()
    licence = auth_token.get_authenticated_licence()

    print(JWKS_EXP_TIME)
    print(os.getenv('PBL_JWKS_LAST_UPDATE'))

    print(auth_token)
    print(user)
    print(licence)
