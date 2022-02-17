from __future__ import annotations

from typing import List

from app.domain import entity, usecases
from fastapi import APIRouter
from pydantic import BaseModel

from . import payloads


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
    __conversations: usecases.Conversation

    def __init__(self, usecase: usecases.Player, conversationUsecase: usecases.Conversation):
        Players.__uc = usecase
        Players.__conversations = conversationUsecase

    @staticmethod
    @ep.post(
        "",
        responses={
            500: {"model": payloads.Errors.Base},
            400: {"model": payloads.Errors.InvalidData},
        },
    )
    async def create_player(player: PlayerBody):
        Players.__uc.new(player.to_entity())

        return "."

    @staticmethod
    @ep.get("", response_model=List[PlayerBody], responses={500: {"model": payloads.Errors.Base}})
    async def list_players():
        return [PlayerBody.from_entity(player) for player in Players.__uc.list()]

    @staticmethod
    @ep.get(
        "/{player_id}",
        response_model=PlayerBody,
        responses={
            500: {"model": payloads.Errors.Base},
            404: {"model": payloads.Errors.NotFound},
        },
    )
    async def get_player(player_id: str):
        return Players.__uc.get(player_id)

    @staticmethod
    @ep.get(
        "/{player_id}/conversations",
        response_model=List[payloads.Conversation],
        tags=["players", "social", "conversations"],
        responses={500: {"model": payloads.Errors.Base}},
    )
    async def list_player_conversations(player_id: str):
        return Players.__conversations.list_for_player(player_id)
