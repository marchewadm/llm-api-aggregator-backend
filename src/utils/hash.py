from passlib.context import CryptContext


class HashUtil:
    """
    A utility class for hashing and verifying secrets.
    """

    def __init__(self) -> None:
        """
        Initializes the hash utility class with the bcrypt context.

        Returns:
            None
        """

        self.bcrypt_context = CryptContext(
            schemes=["bcrypt"], deprecated="auto"
        )

    def create_hash(self, secret: str) -> str:
        """
        Creates a hash from a secret.

        Args:
            secret (str): The secret to hash.

        Returns:
            str: The hashed secret.
        """

        return self.bcrypt_context.hash(secret)

    def verify_hash(self, secret: str, compare_hash: str) -> bool:
        """
        Verifies a secret against a hash.

        Args:
            secret (str): The secret to verify.
            compare_hash (str): The hash to compare the secret against.

        Returns:
            bool: Whether the secret matches the hash.
        """

        return self.bcrypt_context.verify(secret, compare_hash)


hash_util = HashUtil()
