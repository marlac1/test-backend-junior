"""
Initialize and manage dependencies injection.
Can be converted to a package if required.
"""
import logging

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    Configuration,
    Container,
    DependenciesContainer,
    Factory,
    Singleton,
)
from dependency_injector.wiring import Provide
from sqlalchemy.engine import Engine, create_engine

from app.adapters import stores
from app.core import logger
from app.domain import usecases
from app.routes import API
from app.routes import base as base_ep
from app.routes import middlewares, players, social


######### MASKED SETUPS #########
def _setup_sqlalch(config) -> Engine:
    database = config["db"]["name"]

    return create_engine(f"sqlite:///{database}", future=True, echo=True)


def _setup_logging(config) -> None:
    handlers = [logging.StreamHandler()]  # set default logger to console

    logging.basicConfig(
        format='{"level": "%(levelname)s", "name": "%(name)s", "at": "%(asctime)s", %(message)s}',  # noqa: E501
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=logging.getLevelName(config["log"]["level"]),
        force=True,
        handlers=handlers,
    )
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


######### DEPENCIES CONTAINERS #########
class Core(DeclarativeContainer):
    config = Configuration()

    logging = Singleton(_setup_logging, config)
    logger = Singleton(logger.Log, config)

    # ----------------------------------------
    # Database
    # ----------------------------------------
    db = Singleton(_setup_sqlalch, config)


class Store(DeclarativeContainer):
    core: Core = DependenciesContainer()  # type: ignore

    transaction = Factory(stores.SQLTransactions, core.db)

    players = Factory(stores.Players, transaction)
    conversations = Factory(stores.Conversation, transaction)


class Usecases(DeclarativeContainer):
    core: Core = DependenciesContainer()  # type: ignore
    store: Store = DependenciesContainer()  # type: ignore

    players = Singleton(usecases.Player, store.players, core.logger)
    conversations = Singleton(
        usecases.Conversation, store.conversations, store.players, core.logger
    )


class Middlewares(DeclarativeContainer):
    core: Core = DependenciesContainer()  # type: ignore

    checks = Singleton(middlewares.Checks, core.config)


class Endpoints(DeclarativeContainer):
    uc: Usecases = DependenciesContainer()  # type: ignore

    base = Singleton(base_ep.Base)
    players = Singleton(players.Players, uc.players, uc.conversations)
    conversations = Singleton(social.Conversations, uc.conversations)
    messages = Singleton(social.Messages, uc.conversations)


######### APPLICATION CONTAINERS #########
class BoyAPI(DeclarativeContainer):
    config = Configuration()

    core: Core = Container(Core, config=config)  # type: ignore
    store: Store = Container(Store, core=core)  # type: ignore
    middlewares: Middlewares = Container(Middlewares, core=core)  # type: ignore
    uc: Usecases = Container(Usecases, core=core, store=store)  # type: ignore
    endpoints: Endpoints = Container(Endpoints, uc=uc)  # type: ignore

    # ----------------------------------------
    # Transports
    # ----------------------------------------
    router = Singleton(
        API,
        endpoints.base,
        endpoints.players,
        endpoints.conversations,
        endpoints.messages,
    )


######### IN APP SETUP #########
def setup_api_backgound(
    _log=Provide[BoyAPI.core.logging],
    _middlewares=Provide[BoyAPI.middlewares.checks],
):
    pass
