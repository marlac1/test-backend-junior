from __future__ import annotations

from http import HTTPStatus
from typing import List

from app.core import Context
from app.domain import usecases
from fastapi import APIRouter, Depends, Request

from . import payloads
from .middlewares import Checks


class Conversations:
    ep = APIRouter(
        prefix="/social/conversations",
        tags=["social", "conversations"],
        dependencies=[Depends(Checks.token)],
    )

    __uc: usecases.Conversation

    def __init__(self, usecase: usecases.Conversation):
        Conversations.__uc = usecase

    @staticmethod
    @ep.post(
        "/",
        status_code=HTTPStatus.CREATED,
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
            403: {"model": payloads.Errors.Base},
        },
    )
    async def get_conversation(conversation_id: str):
        return Conversations.__uc.get(conversation_id)

    @staticmethod
    @ep.post("/{conversation_id}/read", response_model=payloads.Conversation)
    async def set_read(request: Request, conversation_id: str):
        ctx = Context.new_from_request(request)
        player_id = request.state.player["id"]

        return Conversations.__uc.read(ctx, player_id, conversation_id)

    @staticmethod
    @ep.post("/{conversation_id}/mask", response_model=payloads.Conversation)
    async def mask_conversation(request: Request, conversation_id: str):
        ctx = Context.new_from_request(request)
        masked_by = request.state.player["id"]

        return Conversations.__uc.toggle_mask(ctx, conversation_id, masked_by)


class Messages:
    ep = APIRouter(
        prefix="/social/conversations/{conversation_id}/messages",
        tags=["social", "message", "conversations"],
        dependencies=[Depends(Checks.token)],
    )

    __uc: usecases.Conversation

    def __init__(self, usecase: usecases.Conversation):
        Messages.__uc = usecase

    @staticmethod
    @ep.post(
        "/send",
        status_code=HTTPStatus.CREATED,
        responses={
            500: {"model": payloads.Errors.Base},
            403: {"model": payloads.Errors.Base},
            404: {"model": payloads.Errors.NotFound},
            400: {"model": payloads.Errors.InvalidData},
        },
        response_model=payloads.Message,
    )
    async def send_message(request: Request, conversation_id: str, body: payloads.Message.Send):
        ctx = Context.new_from_request(request)
        player_id = request.state.player["id"]

        return payloads.Message.from_entity(
            Messages.__uc.send_message(ctx, body.to_entity(conversation_id, player_id))
        )

    @staticmethod
    @ep.get(
        "/",
        responses={
            500: {"model": payloads.Errors.Base},
            403: {"model": payloads.Errors.Base},
            400: {"model": payloads.Errors.InvalidData},
            404: {"model": payloads.Errors.NotFound},
        },
        response_model=List[payloads.Message],
    )
    async def list_messages(request: Request, conversation_id: str):
        ctx = Context.new_from_request(request)
        player_id = request.state.player["id"]

        return [
            payloads.Message.from_entity(message)
            for message in Messages.__uc.list_mesages(ctx, conversation_id, player_id)
        ]
