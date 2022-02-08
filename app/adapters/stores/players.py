from statistics import mode
from typing import List
from uuid import UUID

from app.domain import entity
from app.domain.errors import ErrInvalidData, ErrNotFound
from app.domain.interfaces import store
from pyexpat import model
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.sql.expression import select

from ._sql_alch import get_details
from .models import models


class Players(store.Players):
    def __init__(self, transaction: store.Transactions):
        self.__transaction = transaction

    def select(self, player_id: str) -> entity.Player:
        tx = self.__transaction.start()

        query = select(models.Player)
        try:
            UUID(player_id, version=4)
            query = query.where(models.Player.id == player_id)
        except ValueError:
            query = query.where(models.Player.nickname == player_id)

        try:
            player = tx.instance().execute(query).first()
        except NoResultFound:
            raise ErrNotFound("player")
        except Exception as e:
            raise e
        else:
            if not player:
                raise ErrNotFound("player")

            return player[0].to_entity()
        finally:
            tx.clear()

    def list(self) -> List[entity.Player]:
        tx = self.__transaction.start()

        query = select(models.Player)

        try:
            _players = tx.instance().execute(query).scalars()
        except NoResultFound:
            return []
        except Exception as e:
            raise e
        else:
            return [player.to_entity() for player in _players]
        finally:
            tx.clear()

    def insert(self, player: entity.Player):
        tx = self.__transaction.start()

        player = models.Player.from_entity(player, is_update=False)

        tx.instance().add(player)

        try:
            tx.instance().flush()
            tx.commit()
        except IntegrityError as e:
            tx.rollback()
            detail = get_details(str(e.orig))
            raise ErrInvalidData("player", "invalid_request", details=[detail] if detail else None)
        except Exception as e:
            tx.rollback()
            raise e
