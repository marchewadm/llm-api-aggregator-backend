import os
import secrets
import string


def generate_strong_passphrase(length: int = 128) -> str:
    """
    Generates a strong passphrase with the specified length.

    Args:
        length (int): The length of the passphrase. Defaults to 128.

    Returns:
        str: The generated passphrase.
    """

    characters = string.ascii_letters + string.digits + string.punctuation
    passphrase = "".join(secrets.choice(characters) for i in range(length))

    return passphrase


def generate_salt(size: int = 16) -> bytes:
    """
    Generates a random salt.

    Returns:
        bytes: The generated salt.
    """

    salt = os.urandom(size)
    return salt
