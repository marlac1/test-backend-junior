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


class Conversation(store.Conversations):
    def __init__(self, transaction: store.Transactions):
        self.__transaction = transaction

    def select(self, conversation_id: str) -> entity.Conversation:
        tx = self.__transaction.start()

        try:
            conversation = (
                tx.instance()
                .execute(
                    select(models.Conversation).where(models.Conversation.id == conversation_id)
                )
                .first()
            )
        except NoResultFound:
            raise ErrNotFound("conversation")
        except Exception as e:
            raise e
        else:
            if not conversation:
                raise ErrNotFound("conversation")

            return conversation[0].to_entity()
        finally:
            tx.clear()

    def list_for_players(self, player_id: str) -> List[entity.Conversation]:
        tx = self.__transaction.start()
        try:
            _converasations = (
                tx.instance()
                .execute(
                    select(models.Conversation)
                    .join(models.ConversationPlayer)
                    .where(models.ConversationPlayer.player_id == player_id)
                )
                .scalars()
            )
        except NoResultFound:
            return []
        except Exception as e:
            raise e
        else:
            return [conversation.to_entity() for conversation in _converasations]
        finally:
            tx.clear()

    def insert(self, conversation: entity.Conversation):
        tx = self.__transaction.start()

        tx.instance().add(models.Conversation.from_entity(conversation, is_update=False))

        try:
            tx.instance().flush()
        except IntegrityError as e:
            tx.rollback()
            detail = get_details(str(e.orig))
            raise ErrInvalidData(
                "conversation", "invalid_request", details=[detail] if detail else None
            )
        except Exception as e:
            tx.rollback()
            raise e

        for player in conversation.players:
            tx.instance().add(
                models.ConversationPlayer(conversation_id=conversation.id, player_id=player.id)
            )
            try:
                tx.instance().flush()
            except IntegrityError as e:
                tx.rollback()
                detail = get_details(str(e.orig))
                raise ErrInvalidData(
                    "conversation_player", "invalid_request", details=[detail] if detail else None
                )
            except Exception as e:
                tx.rollback()
                raise e

        try:
            tx.commit()
        except Exception as e:
            tx.rollback()
            raise e

    def update(self, conversation: entity.Conversation):
        raise NotImplementedError()
