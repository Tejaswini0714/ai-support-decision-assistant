import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.auth import (
    create_access_token,
    get_user_id_from_token,
    hash_password,
    verify_password,
)


def test_password_hashing():
    password = "test_password"

    password_hash = hash_password(password)

    assert password_hash != password
    assert verify_password(password, password_hash)
    assert not verify_password("wrong_password", password_hash)


def test_jwt_token():
    user_id = 123

    token = create_access_token(user_id)

    assert isinstance(token, str)
    assert get_user_id_from_token(token) == user_id