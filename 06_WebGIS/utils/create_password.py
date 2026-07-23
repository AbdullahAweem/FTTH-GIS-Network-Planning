import bcrypt


def create_password_hash(password: str) -> str:
    """Return a secure bcrypt hash for a password."""
    if not password:
        raise ValueError("Password cannot be empty.")

    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password.decode("utf-8")


if __name__ == "__main__":
    entered_password = input("Enter the password to hash: ").strip()

    try:
        password_hash = create_password_hash(entered_password)
        print("\nPassword hash:\n")
        print(password_hash)
    except ValueError as exc:
        print(f"Error: {exc}")