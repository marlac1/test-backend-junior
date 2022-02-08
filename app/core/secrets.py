from math import floor
from random import random


class Generate:
    """Group all methods to generate new secrets"""

    ALPHA_NUMERIC = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    UPPER_ALPHA_NUMERIC = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    NUMERIC = "0123456789"

    @staticmethod
    def otp(chars=UPPER_ALPHA_NUMERIC) -> str:
        """
        Generate a one time validation code using provided chars set.
        """

        OTP = ""
        length = len(chars)

        for i in range(6):
            OTP += chars[floor(random() * length)]

        return OTP
