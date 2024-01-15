from bcrypt import hashpw, gensalt, checkpw


def hash_password(password: str) -> str:
    encoded = password.encode('utf-8')
    return hashpw(encoded, gensalt()).decode('utf-8')


def check_password(password: str, hashed: str) -> bool:
    encoded_password = password.encode('utf-8')
    # Ensure the hashed password is also encoded
    encoded_hashed = hashed.encode('utf-8')
    return checkpw(encoded_password, encoded_hashed)
