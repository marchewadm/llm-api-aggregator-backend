import os
import base64
import string
import secrets
import binascii

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class PassphraseUtil:
    """
    A utility class for storing methods related to passphrases such as generating secure keys from passphrases and
    salts, converting bytes to hex and vice versa.
    """

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def generate_salt(size: int = 16) -> bytes:
        """
        Generates a random salt.

        Args:
            size (int): The size of the salt. Defaults to 16.

        Returns:
            bytes: The generated salt.
        """

        salt = os.urandom(size)
        return salt

    @staticmethod
    def generate_fernet_key(passphrase: bytes, salt: bytes) -> Fernet:
        """
        Generates a Fernet key from a passphrase and salt.

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

        f_key = Fernet(key)
        return f_key


passphrase_util = PassphraseUtil()
