from __future__ import annotations

from typing import List

from app.domain import entity
from app.domain.errors import Details
from pydantic import BaseModel


class Conversation(BaseModel):
    class Create(BaseModel):
        player_ids: List[str]

    id: str
    archived: bool
    players: List[entity.Player]

    @staticmethod
    def from_entity(player: entity.Conversation) -> Conversation:
        return Conversation(**player.dict(exclude={"id"}))

    def to_entity(self, id: str = "") -> entity.Conversation:
        data = self.dict()
        if id:
            data["id"] = id

        return entity.Conversation(**data)


class Errors:
    class Base(BaseModel):
        error: str

    class NotFound(Base):
        key: str

    class InvalidData(Base):
        key: str
        details: List[Details]
