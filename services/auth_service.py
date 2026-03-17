from datetime import datetime, timedelta, UTC
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from models import User
from config import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(p): return pwd_context.hash(p)
def verify_password(plain, hashed): return pwd_context.verify(plain, hashed)

def create_access_token(data: dict) -> str:
    payload = {**data, "exp": datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

def decode_token(token: str) -> dict:
    try: return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token invalido ou expirado",
                            headers={"WWW-Authenticate": "Bearer"})

async def get_user_by_username(db: AsyncSession, username: str):
    r = await db.execute(select(User).where(User.username == username))
    return r.scalars().first()

async def create_user(db: AsyncSession, username: str, email: str, password: str) -> User:
    r = await db.execute(select(User).where(User.username == username))
    if r.scalars().first(): raise HTTPException(400, "Username ja em uso")
    r = await db.execute(select(User).where(User.email == email))
    if r.scalars().first(): raise HTTPException(400, "Email ja em uso")
    user = User(username=username, email=email, hashed_password=hash_password(password))
    db.add(user); await db.flush(); await db.refresh(user)
    return user

async def authenticate_user(db: AsyncSession, username: str, password: str) -> User:
    user = await get_user_by_username(db, username)
    dummy = "$2b$12$KIXdummyhashfordummyverification1234567890123456789012"
    if not user:
        verify_password("dummy", dummy)
        raise HTTPException(401, "Credenciais invalidas")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(401, "Credenciais invalidas")
    if not user.is_active: raise HTTPException(403, "Conta desativada")
    return user
