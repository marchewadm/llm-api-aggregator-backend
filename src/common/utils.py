import binascii
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def convert_bytes_to_hex(data: bytes) -> str:
    """
    Converts bytes to hexadecimal.

    Args:
        data (bytes): The data to convert.

    Returns:
        str: The hexadecimal representation of the data.
    """

    hex_data = binascii.hexlify(data).decode("utf-8")
    return hex_data


def convert_hex_to_bytes(data: str) -> bytes:
    """
    Converts hexadecimal to bytes.

    Args:
        data (str): The data to convert.

    Returns:
        bytes: The bytes representation of the data.
    """

    bytes_data = binascii.unhexlify(data.encode())
    return bytes_data


def generate_secure_key(passphrase: bytes, salt: bytes) -> bytes:
    """
    Generates a secure key from a passphrase and salt.

    Args:
        passphrase (bytes): The passphrase to generate the key from.
        salt (bytes): The salt to use in the key generation.

    Returns:
        bytes: The generated key.
    """

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt, iterations=600000
    )
    key = base64.urlsafe_b64encode(kdf.derive(passphrase))

    return key
