from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from core.security import authenticate_user, create_access_token

router = APIRouter()

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticates a user and returns a JWT access token.

    This endpoint validates the provided username and password using OAuth2 standards.
    If the credentials are valid, it returns a JWT token that can be used to authenticate
    subsequent requests.

    Args:
        form_data (OAuth2PasswordRequestForm): Form data containing 'username' and 'password'.

    Raises:
        HTTPException: If the username or password is incorrect.

    Returns:
        dict: A dictionary with the access token and token type.
            Example:
            {
                "access_token": "<jwt_token_string>",
                "token_type": "bearer"
            }
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )

    access_token = create_access_token(data={"sub": user})
    return {"access_token": access_token, "token_type": "bearer"}
