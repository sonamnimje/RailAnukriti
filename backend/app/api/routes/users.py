from datetime import timedelta, datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.db.models import User


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "controller"


class UserRead(BaseModel):
    id: int
    username: str
    role: str


def hash_password(raw_password: str) -> str:
    return password_context.hash(raw_password)


def verify_password(raw_password: str, hashed_password: str) -> bool:
    return password_context.verify(raw_password, hashed_password)


def create_access_token(subject: str, role: str, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"sub": subject, "role": role, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")  # type: ignore[assignment]
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user: User | None = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


def require_role(*allowed_roles: str):
    def dependency(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return dependency


@router.post("/signup", response_model=UserRead)
def signup(payload: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    existing = db.query(User).filter(User.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(
        username=payload.username,
        hashed_password=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserRead(id=user.id, username=user.username, role=user.role)


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    user: User | None = db.query(User).filter(User.username == form_data.username).first()
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(str(user.username), user.role)
    return Token(access_token=access_token)


@router.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_user)) -> UserRead:
    return UserRead(id=current_user.id, username=current_user.username, role=current_user.role)


