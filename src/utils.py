from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_hash(secret: str) -> str:
    """
    Creates a hash from a secret.

    Args:
        secret (str): The secret to hash.

    Returns:
        str: The hashed secret.
    """

    return bcrypt_context.hash(secret)


def verify_hash(secret: str, compare_hash: str) -> bool:
    """
    Verifies a secret against a hash.

    Args:
        secret (str): The secret to verify.
        compare_hash (str): The hash to compare the secret against.

    Returns:
        bool: Whether the secret matches the hash.
    """

    return bcrypt_context.verify(secret, compare_hash)
