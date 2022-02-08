from typing import List
from uuid import uuid4

from app.core import Log
from app.domain import entity
from app.domain.errors import ErrInvalidData, ErrNotFound, ErrUnexpected
from app.domain.interfaces import store


class Player:
    def __init__(self, store: store.Players, log: Log):
        self.__log = log.named("usecases.player")
        self.__store = store

    def get(self, player_id: str) -> entity.Player:
        log = self.__log.method("get").parameter("player_id", player_id)

        try:
            player = self.__store.select(player_id)
        except ErrNotFound as e:
            log.exception(e).info("Unexistant")
            raise e
        except Exception as e:
            log.error("Could not read storage", e)
            raise ErrUnexpected().to_precise("CannotReadPlayer") from e
        else:
            log.success()
            return player

    def list(self) -> List[entity.Player]:
        log = self.__log.method("list")

        try:
            players = self.__store.list()
        except Exception as e:
            log.error("Could not read storage", e)
            raise ErrUnexpected().to_precise("CannotReadPlayer") from e
        else:
            log.success()
            return players

    def new(self, player: entity.Player):
        log = self.__log.method("new").parameter("to_create", player)

        player.id = str(uuid4())

        try:
            self.__store.insert(player)
        except ErrInvalidData as e:
            log.exception(e).info("Invalid player")
            raise e
        except Exception as e:
            log.error("Could not insert", e)
            raise ErrUnexpected().to_precise("CannotInsertPlayer") from e
        else:
            log.success()
