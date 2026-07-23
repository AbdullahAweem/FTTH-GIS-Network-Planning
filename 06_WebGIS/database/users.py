import bcrypt
import pandas as pd
from database.connection import get_postgres_engine


def get_user_by_username(username: str):
    """
    Get one active user from PostgreSQL by username.
    """
    if not username:
        return None
    engine = get_postgres_engine()
    sql = """
        SELECT
            u.user_id,
            u.username,
            u.password_hash,
            u.full_name,
            r.role_name
        FROM security.users AS u
        JOIN security.roles AS r
            ON u.role_id = r.role_id
        WHERE
            LOWER(u.username) = LOWER(%s)
            AND u.is_active = TRUE
        LIMIT 1;
    """
    df = pd.read_sql(sql, engine, params=(username,))
    if df.empty:
        return None
    return df.iloc[0].to_dict()


def verify_password(password: str, password_hash: str) -> bool:
    """
    Compare typed password with stored bcrypt hash.
    """
    if not password or not password_hash:
        return False
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash.encode("utf-8")
        )
    except Exception:
        return False


def authenticate_user(username: str, password: str):
    """
    Return user details if login is valid.
    Otherwise return None.
    """
    user = get_user_by_username(username)
    if user is None:
        return None
    if verify_password(password, user["password_hash"]):
        return {
            "user_id": user["user_id"],
            "username": user["username"],
            "name": user["full_name"],
            "role": user["role_name"],
        }
    return None