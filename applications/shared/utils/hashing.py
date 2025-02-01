from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, HashingError


password_hasher= PasswordHasher()


def hash_password(password:str)-> str:
    """
    Hashes a given string using Argon2.
    :returns: A hashed string.
    :raises: HashingError if hash failed.
    """
    try:
        return password_hasher.hash(password)
    except HashingError:
        raise

def verify_password(password:str, hashed_password:str)-> bool:
    """
    Checks a given string if matches with hashed string.
    :returns: True if strings match | False if not.
    :raises: VerifyMismatchError if verification fails.
    """
    try:
        return password_hasher.verify(hashed_password, password)
    except VerifyMismatchError:
        return False

# ------------
# UTILITY TEST
# ------------

#password= hash_password('caintheterrible')
#print(password)

#check= verify_password('caintheterrible', password)
#print(check)