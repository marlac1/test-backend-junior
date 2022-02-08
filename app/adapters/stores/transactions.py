from app.domain.interfaces import store
from sqlalchemy.orm import Session


class ErrNoTransaction(Exception):
    def __init__(self, prefix: str = ""):
        if prefix:
            prefix += ": "
        super().__init__(prefix + "no transaction in progress")


class ErrCommitted(Exception):
    def __init__(self, prefix: str = ""):
        super().__init__(prefix + "transaction was committed")


class ErrRollbacked(Exception):
    def __init__(self, prefix: str = ""):
        super().__init__(prefix + "transaction was rollbacked")


class SQLTransactions(store.Transactions):
    __session: Session = None  # TODO check impact of recreating sessions here

    def __init__(self, engine):
        self.__engine = engine
        self.__rollbacked = False
        self.__committed = False

    # def __del__(self):
    #     self.clear

    def start_read_related(self) -> store.Transactions:
        raise NotImplementedError("StartReadRelatedNotSQLSupported")

    def start(self) -> store.Transactions:
        tx = SQLTransactions(self.__engine)
        tx.clear()
        tx.__session = Session(self.__engine)

        return tx

    def commit(self) -> None:
        self.ready(is_commit=True)

        self.__session.commit()
        self.__session.close()
        self.__session = None
        self.__committed = True

    def rollback(self) -> None:
        self.ready(is_rollback=True)

        self.__session.rollback()
        self.__session.close()
        self.__session = None
        self.__rollbacked = True

    def instance(self) -> Session:
        if not self.__session:
            self.__session = Session(self.__engine)

        return self.__session

    def ready(self, is_commit: bool = False, is_rollback: bool = False):
        prefix = ""

        if is_commit:
            prefix = "cannot commit"
        elif is_rollback:
            prefix = "cannot rollback"

        if not is_commit and self.__committed:
            raise ErrCommitted(prefix)

        if not is_rollback and self.__rollbacked:
            raise ErrRollbacked(prefix)

        if not self.__session:
            raise ErrNoTransaction(prefix)

    def clear(self) -> None:
        if self.__session:
            try:
                self.__session.expire_all()
                self.__session.close()
            except:  # nosec # noqa: E722
                pass

        self.__session = None
        self.__rollbacked = False
        self.__committed = False
