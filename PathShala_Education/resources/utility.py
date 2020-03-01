# Todo: MARK: Used to encrypt the hash/pseudo code.


from enum import Enum


# TODO : This function consists of Mail type enum
#       - Registration Mail
#       - Send Otp
#       - Other Mail


class EmailType(Enum):
    REGISTRATION = "Registration Mail"
    OTP = "Send Otp"
    OTHER = "Other Mail"
