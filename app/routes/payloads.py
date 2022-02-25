from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from app.domain import entity
from app.domain.errors import Details
from pydantic import BaseModel


class Conversation(BaseModel):
    class Create(BaseModel):
        player_ids: List[str]

    id: str
    archived: bool
    players: List[entity.Player]
    masked_by: List[str] = []
    latest_read_message: Dict[str, str] = {}

    @staticmethod
    def from_entity(player: entity.Conversation) -> Conversation:
        return Conversation(**player.dict(exclude={"id"}))

    def to_entity(self, id: str = "") -> entity.Conversation:
        data = self.dict()
        if id:
            data["id"] = id

        return entity.Conversation(**data)


class Message(BaseModel):
    id: str
    conversation_id: str
    send_by: str
    content: str
    attachments: Dict
    metadata: Dict
    at: datetime

    class Send(BaseModel):
        content: str
        attachments: Dict = {}
        at: datetime

        def to_entity(self, conversation_id: str, player_id: str) -> entity.Conversation.Message:
            data = self.dict()
            data["conversation_id"] = conversation_id
            data["send_by"] = player_id
            data["send_at"] = data["at"]

            return entity.Conversation.Message(**data)

    @staticmethod
    def from_entity(message: entity.Conversation.Message) -> Message:
        data = message.dict()
        data["at"] = message.send_at

        return Message(**data)


class Errors:
    class Base(BaseModel):
        error: str

    class NotFound(Base):
        key: str

    class InvalidData(Base):
        key: str
        details: List[Details]
