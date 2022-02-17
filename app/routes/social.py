from __future__ import annotations

from typing import List

from app.domain import entity, usecases
from fastapi import APIRouter
from pydantic import BaseModel

from . import payloads


class Conversations:
    ep = APIRouter(prefix="/social/conversations", tags=["social", "conversations"])

    __uc: usecases.Conversation

    def __init__(self, usecase: usecases.Conversation):
        Conversations.__uc = usecase

    @staticmethod
    @ep.post(
        "/",
        response_model=payloads.Conversation,
        responses={
            500: {"model": payloads.Errors.Base},
            400: {"model": payloads.Errors.InvalidData},
        },
    )
    async def create_conversation(
        conversation: payloads.Conversation.Create,
    ):
        return Conversations.__uc.new(conversation.player_ids)

    @staticmethod
    @ep.get(
        "/{conversation_id}",
        response_model=payloads.Conversation,
        responses={
            500: {"model": payloads.Errors.Base},
            404: {"model": payloads.Errors.NotFound},
        },
    )
    async def get_conversation(conversation_id: str):
        return Conversations.__uc.get(conversation_id)

    # @staticmethod
    # @ep.post("/{conversation_id}/read", response_model=ConversationBody)
    # async def set_read(conversation_id: str):
    #     return Conversations.__uc.new(conversation.to_entity())

    # @staticmethod
    # @ep.post("/{conversation_id}/player/{player_id}/block", response_model=ConversationBody)
    # async def block_player(conversation_id: str, player_id: str):
    #     return Conversations.__uc.new(conversation.to_entity())
