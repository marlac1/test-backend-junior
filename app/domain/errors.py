from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import Any, List, Optional

from app.core.stringcase import pascalcase  # type: ignore
from pydantic import BaseModel


def _new_precise_error(from_exception: type, new_name: str, *args, **kwargs):
    def constructor(self, *args, **kwargs):
        from_exception.__init__(self, *args, **kwargs)

    new_name = pascalcase(new_name)
    err_cls = type(new_name, (from_exception,), {"__init__": constructor, "__super": None})
    return err_cls(*args, **kwargs)


class BetException(Exception, ABC):
    status: int = HTTPStatus.IM_A_TEAPOT

    @abstractmethod
    def to_json(self) -> dict:
        """Format error to json"""

    @abstractmethod
    def to_precise(self, new_name: str):
        """Precise error using new class for Sentry logging"""
        raise NotImplementedError()


class ErrUnexpected(BetException):
    """
    ErrUnexpected represents global exception for errors that should not happen
    and we don't wish to provide information to end user.
    """

    status = HTTPStatus.INTERNAL_SERVER_ERROR

    def to_json(self) -> dict:
        return {
            "error": "something unexpected happened",
        }

    def to_precise(self, new_name):
        return _new_precise_error(type(self), new_name)


class ErrNonBlockingUnexpected(BetException):
    """
    ErrUnexpected represents global exception for errors that should not happen
    and we don't wish to provide information to end user.
    """

    status = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, key: str = "something unexpected happened"):
        self.__error = key

    def to_json(self) -> dict:
        return {
            "error": self.__error,
        }

    def to_precise(self, new_name):
        return _new_precise_error(type(self), new_name, self.__error)


class ErrUnauthorized(BetException):
    """
    ErrUnauthorized represents authorization erros that happen when a login status
    is required but none exists.
    """

    status = HTTPStatus.UNAUTHORIZED

    def __init__(self, message: str = "Unauthorized"):
        self.__error = message

    def to_json(self) -> dict:
        return {
            "error": self.__error,
        }

    def to_precise(self, new_name: str):
        return _new_precise_error(type(self), new_name)


class ErrTooManyRequest(BetException):
    """
    ErrUnauthorized represents authorization erros that happen when a login status
    is required but none exists.
    """

    status = HTTPStatus.TOO_MANY_REQUESTS

    def __init__(self, message: str = "Too many requests"):
        self.__error = message

    def to_json(self) -> dict:
        return {
            "error": self.__error,
        }

    def to_precise(self, new_name: str):
        return _new_precise_error(type(self), new_name)


class ErrNotFound(BetException):
    """
    ErrUnotFound has to be raised if data was expected but
    not does not exits.
    """

    status = HTTPStatus.NOT_FOUND

    def __init__(self, key: str):
        self.__key = key
        self.__error = "not_found"

        super().__init__(f"Invalid{pascalcase(key)}: {self.__error}")

    def to_json(self) -> dict:
        return {"key": self.__key, "error": self.__error}

    def to_precise(self, _: str):
        return _new_precise_error(type(self), f"{pascalcase(self.__key)}NotFound", self.__key)


class Details(BaseModel):
    """
    Details represent a detailed error information to return to the user.
    """

    key: str
    message: str
    value: Optional[Any] = None


class ErrInvalidData(BetException):
    """
    ErrInvalidData propagate invalid data informations.
    """

    def __init__(self, key: str, error: str, details: List[Details] = None):
        self.__key = key
        self.__error = error
        self.__details = details
        self.status = HTTPStatus.BAD_REQUEST

        super().__init__(f"Invalid{pascalcase(key)}: {error}")

    @property
    def main_error(self) -> str:
        return self.__error

    def to_json(self) -> dict:
        return {
            "key": self.__key,
            "error": self.__error,
            "details": [detail.dict() for detail in self.__details] if self.__details else None,
        }

    def to_precise(self, _: str):
        return _new_precise_error(
            type(self),
            f"Invalid{pascalcase(self.__key)}",
            key=self.__key,
            error=self.__error,
            details=self.__details,
        )


class ErrUnexpectedResponse(Exception):
    """
    Error raised when service did
    not return expected responses
    """


class ErrInvalidResponseFormat(Exception):
    """
    Error raised when service did not
    return a parsable error.
    """
