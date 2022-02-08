from datetime import datetime

from fastapi import APIRouter


class Base:
    ep = APIRouter(prefix="")

    @staticmethod
    @ep.api_route("/", methods=["GET", "HEAD", "OPTIONS"])
    @ep.api_route("/ping", methods=["GET", "HEAD", "OPTIONS"])
    async def ping_server():
        return "."

    @staticmethod
    @ep.api_route("/utc", methods=["GET", "HEAD", "OPTIONS"])
    async def ping_utc():
        return datetime.utcnow().strftime("%d/%m/%y - %H:%M")
