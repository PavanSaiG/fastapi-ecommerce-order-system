from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.database.session import get_db
from app.config import settings
from app.models.user import User

# Authentication & Authorization using OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# Dependency Injection for API key validation
def get_api_key(api_key: str = Header(None)):
    if api_key != "secret-api-key":
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Dependency to get the current authenticated user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user
