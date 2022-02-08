from enum import Enum


class OS(str, Enum):
    iOS = "IOS"
    Android = "ANDROID"


class ReservedAdmin:
    SYSTEM = "SYSTEM"
    BOY = "BetOnYou"
    BOY_BOT = "BetOnYou auto"
    BOY_BOT_ID = "BetOnYouAuto"
