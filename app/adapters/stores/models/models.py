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

    @staticmethod
    def from_entity(conversation: entity.Conversation, is_update: bool = True):
        data = (
            conversation.dict(include=conversation.updated_fields(), exclude={"players"})
            if is_update
            else conversation.dict(exclude={"players"})
        )
        return Conversation(**data)

    def to_entity(self) -> entity.Conversation:
        return entity.Conversation(
            id=self.id,
            archived=self.archived,
            created_at=self.created_at,
            players=[player.to_entity() for player in self.players],
        )
