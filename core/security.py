from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from data.users import users

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 5))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def authenticate_user(username: str, password: str):
    """
    Validates the given username and password against the registered users.

    Args:
        username (str): The username provided by the client.
        password (str): The password provided by the client.

    Returns:
        str | None: The username if authentication is successful, otherwise None.
    """
    if username in users and users[username] == password:
        return username
    return None


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Generates a JWT access token containing the provided data and expiration.

    Args:
        data (dict): Payload to encode in the token.
        expires_delta (timedelta, optional): Time duration until the token expires. 
            Defaults to the configured ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str = Depends(oauth2_scheme)):
    """
    Verifies a JWT token and extracts the subject (username).

    Args:
        token (str): JWT token automatically extracted by FastAPI via OAuth2PasswordBearer.

    Raises:
        HTTPException: If the token is invalid or does not contain a valid 'sub' claim.

    Returns:
        str: The username extracted from the token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception
