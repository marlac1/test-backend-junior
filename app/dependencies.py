"""
Initialize and manage dependencies injection.
Can be converted to a package if required.
"""
import logging

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (  # DependenciesContainer,
    Configuration,
    Container,
    Singleton,
)
from dependency_injector.wiring import Provide

from app.core import logger
from app.routes import API
from app.routes import base as base_ep

######### MASKED SETUPS #########
# def _setup_sqlalch(config) -> Engine:
#     usr = config["postgres"]["user"]
#     pwd = config["postgres"]["password"]
#     hostname = config["postgres"]["host"]
#     database = config["postgres"]["database"]

#     return create_engine(
#         f"postgresql://{usr}:{pwd}@{hostname}/{database}?sslmode=disable", future=True, echo=True
#     )


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
    # postgres = Singleton(_setup_sqlalch, config)


class Endpoints(DeclarativeContainer):

    base = Singleton(base_ep.Base)


######### APPLICATION CONTAINERS #########
class BoyAPI(DeclarativeContainer):
    config = Configuration()

    core: Core = Container(Core, config=config)  # type: ignore
    endpoints: Endpoints = Container(Endpoints)  # type: ignore

    # ----------------------------------------
    # Transports
    # ----------------------------------------
    router = Singleton(
        API,
        endpoints.base,
    )


######### IN APP SETUP #########
def setup_api_backgound(
    _log=Provide[BoyAPI.core.logging],
    # _middlewares=Provide[BoyAPI.middlewares.checks],
):
    pass
