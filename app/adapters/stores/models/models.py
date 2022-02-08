from os import stat

from app.domain import entity
from sqlalchemy import Column, String

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
