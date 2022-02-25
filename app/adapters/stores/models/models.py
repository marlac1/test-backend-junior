from __future__ import annotations

from datetime import datetime

from app.domain import entity
from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from . import Base


class Player(Base):

    __tablename__ = "players"

    id = Column(String, primary_key=True)
    nickname = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    gender = Column(String)

    @staticmethod
    def from_entity(player: entity.Player, is_update: bool = True):
        data = player.dict(include=player.updated_fields()) if is_update else player.dict()
        return Player(**data)

    def to_entity(self) -> entity.Player:
        return entity.Player(
            id=self.id,
            nickname=self.nickname,
            phone_number=self.phone_number,
            gender=self.gender,
        )


class ConversationMessage(Base):
    __tablename__ = "conversation_messages"

    id = Column(String, primary_key=True)
    send_by = Column(String, ForeignKey("players.id"), nullable=False)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    content = Column(String)
    attachments = Column(JSON)
    _metadata = Column("metadata", JSON)
    send_at = Column(DateTime, default=datetime.utcnow)

    def to_entity(self) -> entity.Conversation.Message:
        return entity.Conversation.Message(
            id=self.id,
            send_by=self.send_by,
            conversation_id=self.conversation_id,
            send_at=self.send_at,
            content=self.content,
            attachments=self.attachments if self.attachments else {},
            metadata=self._metadata if self._metadata else {},
        )

    @staticmethod
    def from_entity(
        message: entity.Conversation.Message, is_update: bool = True
    ) -> ConversationMessage:
        data = message.dict(include=message.updated_fields()) if is_update else message.dict()
        if not data["attachments"]:
            del data["attachments"]

        if not data["metadata"]:
            del data["metadata"]

        return ConversationMessage(**data)


class ConversationPlayer(Base):
    __tablename__ = "conversation_players"

    conversation_id = Column(String, ForeignKey("conversations.id"), primary_key=True)
    player_id = Column(String, ForeignKey("players.id"), primary_key=True)
    last_read = Column(String, ForeignKey("conversation_messages.id"))
    last_sent = Column(String, ForeignKey("conversation_messages.id"))
    masked = Column(Boolean, nullable=False, default=False)


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True)
    archived = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False)

    players = relationship(Player, secondary="conversation_players")
    __conversation_players = relationship(ConversationPlayer)

    @staticmethod
    def from_entity(conversation: entity.Conversation, is_update: bool = True):
        data = (
            conversation.dict(include=conversation.updated_fields(), exclude={"players"})
            if is_update
            else conversation.dict(exclude={"players", "latest_read_message", "masked_by"})
        )
        return Conversation(**data)

    def update(self, conversation: entity.Conversation):
        data = conversation.dict(
            include=conversation.updated_fields(),
            exclude={"players", "latest_read_message", "masked_by"},
        )

        for field, value in data.items():
            setattr(self, field, value)

        return self

    def to_entity(self) -> entity.Conversation:
        return entity.Conversation(
            id=self.id,
            archived=self.archived,
            created_at=self.created_at,
            players=[player.to_entity() for player in self.players],
            masked_by=[
                player.player_id for player in self.__conversation_players if player.masked
            ],
            latest_read_message={
                player.player_id: player.last_read
                for player in self.__conversation_players
                if player.last_read is not None
            },
        )
