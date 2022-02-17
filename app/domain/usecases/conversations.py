from typing import List
from uuid import uuid4

from app.core import Log
from app.domain import entity
from app.domain.errors import ErrInvalidData, ErrNotFound, ErrUnexpected
from app.domain.interfaces import store


class Conversation:
    def __init__(self, store: store.Conversations, playerStore: store.Players, log: Log):
        self.__log = log.named("usecases.conversation")
        self.__store = store
        self.__players = playerStore

    def new(self, player_ids: List[str]) -> entity.Conversation:
        log = self.__log.named("new").parameter("players", player_ids)

        try:
            players = [self.__players.select(player) for player in player_ids]
        except ErrNotFound as e:
            log.exception(e).info("A player does not exists")
            raise e
        except Exception as e:
            log.error("Could not check players", e)
            raise ErrUnexpected().to_precise("CannotCheckPlayers")

        conversation = entity.Conversation(id=str(uuid4()), players=players)

        log.parameter("conversation", conversation)

        try:
            self.__store.insert(conversation)
        except ErrInvalidData as e:
            log.exception(e).info("Invalid conversation")
            raise e
        except Exception as e:
            log.error("Could not insert", e)
            raise ErrUnexpected().to_precise("CannotCreateConversation") from e
        else:
            log.success()
            return conversation

    def get(self, conversation_id: str) -> entity.Conversation:
        log = self.__log.named("get").parameter("conversation", conversation_id)

        try:
            conversation = self.__store.select(conversation_id)
        except ErrNotFound as e:
            log.info("Not found")
            raise e
        except Exception as e:
            log.error("Could not read", e)
            raise ErrUnexpected().to_precise("CannotRetrieveConversation") from e
        else:
            log.success()
            return conversation

    def list_for_player(self, player_id: str) -> List[entity.Conversation]:
        log = self.__log.named("list_for_player").parameter("player_id", player_id)

        try:
            conversations = self.__store.list_for_players(player_id)
        except Exception as e:
            log.error("Could not read", e)
            raise ErrUnexpected().to_precise("CannotRetrieveConversations") from e
        else:
            log.success()
            return conversations
