from .context import Context
from .entities import OS, ReservedAdmin
from .logger import Log

all = [Context, Log, OS, ReservedAdmin]


def rremove(alist, x):
    alist.pop(len(alist) - alist[::-1].index(x) - 1)


def safe_cast(val, to_type, default=None):
    try:
        if val:
            return to_type(val.strip().rstrip("\r\n"))
        else:
            return default
    except (ValueError, TypeError):
        return default
