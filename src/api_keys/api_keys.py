from src.auth.utils import bcrypt_context
from src.common.utils import generate_secure_key
from src.users.crud.crud import get_user_passphrase

from src.database.dependencies import db_dependency
from src.auth.dependencies import auth_dependency
from src.users.schemas.schemas import UserPassphrase

from src.common.utils import convert_hex_to_bytes


def get_user_fernet_key(
    passphrase: UserPassphrase, auth: auth_dependency, db: db_dependency
):
    """"""

    user = get_user_passphrase(db, auth["id"])
    print(user.passphrase_salt)
    test = convert_hex_to_bytes(user.passphrase_salt)
    print(test)

    if not bcrypt_context.verify(passphrase.passphrase, user.passphrase):
        pass

    fernet_key = generate_secure_key(
        passphrase.passphrase.encode(), user.passphrase_salt
    )
    return fernet_key
