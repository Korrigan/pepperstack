"""
Simple utility module to generate random passwords

"""

import os
import string

DEFAULT_PASSWORD_LENGTH = 12
ALLOWED_PASSWORD_CHARS = string.letters + string.digits + string.punctuation

def random_password(length=DEFAULT_PASSWORD_LENGTH):
    """
    Returns a random password of `length` characters

    """
    pw = ''
    for i in range(length):
        idx = int(os.urandom(1)) % len(ALLOWED_PASSWORD_CHARS)
        pw += ALLOWED_PASSWORD_CHARS[idx]
    return pw
