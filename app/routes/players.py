from __future__ import annotations

from typing import List

from app.domain import entity, usecases
from fastapi import APIRouter
from pydantic import BaseModel


class PlayerBody(BaseModel):
    nickname: str
    phone_number: str
    gender: entity.Gender = entity.Gender.OTHERS

    @staticmethod
    def from_entity(player: entity.Player) -> PlayerBody:
        return PlayerBody(**player.dict(exclude={"id"}))

    def to_entity(self, id: str = "") -> entity.Player:
        data = self.dict()
        data["id"] = id

        return entity.Player(**data)


class Players:
    ep = APIRouter(prefix="/players", tags=["players"])

    __uc: usecases.Player

    def __init__(self, usecase: usecases.Player):
        Players.__uc = usecase

    @staticmethod
    @ep.post("")
    async def create_player(player: PlayerBody):
        Players.__uc.new(player.to_entity())

        return "."

    @staticmethod
    @ep.get("", response_model=List[PlayerBody])
    async def list_players():
        return [PlayerBody.from_entity(player) for player in Players.__uc.list()]

    @staticmethod
    @ep.get("/{player_id}", response_model=PlayerBody)
    async def get_player(player_id: str):
        return Players.__uc.get(player_id)
