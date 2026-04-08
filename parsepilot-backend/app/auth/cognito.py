import json
import urllib.request
from functools import lru_cache
from jose import JWT, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings

# Tell FastAPI to look for Authorization: Bearer <Token>
security = HTTPBearer

# Cache keys
@lru_cache
def get_cognito_public_keys():
    """
    Fetches Cognito's JWKS
    Keys verify JWT was issued by Cognito pool
    """
    url = (
        f"https://cognito-idp.{settings.cognito_region}.amazonaws.com"
        f"{settings.cognito_user_pool_id}/.well-known/jwks.json"
    )
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read())

async def get_current_user(
        credentials:
        HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    Dependency function  
    called automatically if `current_user: dict = Depends(get_current_user)`
    in params.
    Extracts JWT from Auth header, verifies JWT & returns decoded token payload
    """
    token = credentials.credentials

    try:
        # Decode JWT using Cognito's public keys
        keys = get_cognito_public_keys()
        payload = jwt.decode(
            token,
            keys,
            algorithms=["RS256"],
            audience=settings.cognito_app_client_id,issuer=
            f"https://cognito-idp.{settings.cognito_region}.amazonaws.com/{settings.cogito_user_pool_id}"
        )
        # Payload contains user details
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
