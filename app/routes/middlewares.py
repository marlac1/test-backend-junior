from logging import getLogger

from app.domain.errors import ErrUnauthorized
from fastapi import Request, Security
from fastapi.security.api_key import APIKeyHeader

__HEADER_KEY_NAME = "access_token"

# Securite par apikey
api_key_header = APIKeyHeader(name=__HEADER_KEY_NAME, auto_error=False)
api_key_header_chatbot = APIKeyHeader(name=__HEADER_KEY_NAME, auto_error=False)


# securite par token
class Checks:
    __config: dict

    @staticmethod
    def __log():
        return getLogger("fastapi.middleware")

    def __init__(self, conf: dict):
        Checks.__config = conf

    @staticmethod
    async def token(request: Request, api_key_header: str = Security(api_key_header)):
        # Validate through API key instead of tokens for Admin requests.
        if api_key_header == Checks.__config["api"]["key"]:
            user = request.headers.get("player_id")
            if user:
                request.state.player = {"id": user}

                return request.state.player
            return api_key_header

        if "Authorization" not in request.headers:
            raise ErrUnauthorized()

    @staticmethod
    async def admin(request: Request, api_key_header: str = Security(api_key_header)):
        # Validate through API key instead of tokens for Admin requests.
        if api_key_header != Checks.__config["api"]["key"]:
            raise ErrUnauthorized()

        user = request.headers.get("player_id")
        if user:
            request.state.player = {"id": user}
            return request.state.player

        return api_key_header
