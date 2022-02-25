from typing import List

from app.domain import entity
from app.domain.errors import ErrInvalidData, ErrNotFound
from app.domain.interfaces import store
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.sql.expression import select, update

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

    def list_messages(self, conversation_id: str) -> List[entity.Conversation.Message]:
        tx = self.__transaction.start()
        try:
            _messages = (
                tx.instance()
                .execute(
                    select(models.ConversationMessage).where(
                        models.ConversationMessage.conversation_id == conversation_id
                    )
                )
                .scalars()
            )
        except NoResultFound:
            return []
        except Exception as e:
            raise e
        else:
            return [message.to_entity() for message in _messages]
        finally:
            tx.clear()

    def get_latest_recieved_message(
        self, conversation_id: str, player_id: str
    ) -> entity.Conversation.Message:
        tx = self.__transaction.start()
        try:
            _messages = (
                tx.instance()
                .execute(
                    select(models.ConversationMessage)
                    .where(
                        models.ConversationMessage.conversation_id == conversation_id,
                        models.ConversationMessage.send_by != player_id,
                    )
                    .order_by(desc(models.ConversationMessage.send_at))
                )
                .first()
            )
        except NoResultFound:
            raise ErrNotFound("Message")
        except Exception as e:
            raise e
        else:
            if not _messages:
                raise ErrNotFound("Message")

            return _messages[0].to_entity()
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

    def update(self, new_conversation: entity.Conversation):
        tx = self.__transaction.start()

        try:
            _conversation = (
                tx.instance()
                .execute(
                    select(models.Conversation).where(
                        models.Conversation.id == new_conversation.id
                    )
                )
                .first()
            )
        except NoResultFound:
            tx.clear()
            raise ErrNotFound("conversation")
        except Exception as e:
            tx.clear()
            raise e
        else:
            if not _conversation:
                tx.clear()
                raise ErrNotFound("conversation")

            model_conversation = _conversation[0]
            conversation: entity.Conversation = _conversation[0].to_entity()

        for player_id in conversation.masked_by:
            if player_id not in new_conversation.masked_by:
                try:
                    (
                        tx.instance().execute(
                            update(models.ConversationPlayer)
                            .where(
                                models.ConversationPlayer.conversation_id == new_conversation.id,
                                models.ConversationPlayer.player_id == player_id,
                            )
                            .values(masked=False)
                        )
                    )
                except IntegrityError as e:
                    tx.rollback()
                    detail = get_details(str(e.orig))
                    raise ErrInvalidData(
                        "conversation_player",
                        "invalid_request",
                        details=[detail] if detail else None,
                    )
                except Exception as e:
                    tx.rollback()
                    raise e

        for player_id in new_conversation.masked_by:
            if player_id not in new_conversation.masked_by:
                try:
                    (
                        tx.instance().execute(
                            update(models.ConversationPlayer)
                            .where(
                                models.ConversationPlayer.conversation_id == new_conversation.id,
                                models.ConversationPlayer.player_id == player_id,
                            )
                            .values(masked=True)
                        )
                    )
                except IntegrityError as e:
                    tx.rollback()
                    detail = get_details(str(e.orig))
                    raise ErrInvalidData(
                        "conversation_player",
                        "invalid_request",
                        details=[detail] if detail else None,
                    )
                except Exception as e:
                    tx.rollback()
                    raise e

        for read_by, message in new_conversation.latest_read_message.items():
            if conversation.latest_read_message.get(read_by, "") != message:
                try:
                    (
                        tx.instance().execute(
                            update(models.ConversationPlayer)
                            .where(
                                models.ConversationPlayer.conversation_id == new_conversation.id,
                                models.ConversationPlayer.player_id == read_by,
                            )
                            .values(last_read=message)
                        )
                    )
                except IntegrityError as e:
                    tx.rollback()
                    detail = get_details(str(e.orig))
                    raise ErrInvalidData(
                        "conversation_player",
                        "invalid_request",
                        details=[detail] if detail else None,
                    )
                except Exception as e:
                    tx.rollback()
                    raise e

        model_conversation.update(new_conversation)

        try:
            tx.commit()
            tx.instance().flush()
            tx.commit()
        except IntegrityError as e:
            tx.rollback()
            detail = get_details(str(e.orig))
            raise ErrInvalidData(
                "conversation_player", "invalid_request", details=[detail] if detail else None
            )
        except Exception as e:
            tx.rollback()
            raise e
        finally:
            tx.clear()

    def add_message(self, message: entity.Conversation.Message):
        tx = self.__transaction.start()

        tx.instance().add(models.ConversationMessage.from_entity(message, is_update=False))

        try:
            tx.instance().flush()
            tx.commit()
        except IntegrityError as e:
            tx.rollback()
            detail = get_details(str(e.orig))
            raise ErrInvalidData(
                "message", "invalid_request", details=[detail] if detail else None
            )
        except Exception as e:
            tx.rollback()
            raise e
        finally:
            tx.clear()
