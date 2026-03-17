from datetime import datetime, UTC
from decimal import Decimal
from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from database import Base

class TransactionType(str, PyEnum):
    DEPOSIT    = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER   = "transfer"

class User(Base):
    __tablename__ = "users"
    id              = Column(Integer, primary_key=True, index=True)
    username        = Column(String(50),  unique=True, nullable=False, index=True)
    email           = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active       = Column(Boolean, default=True, nullable=False)
    created_at      = Column(DateTime, default=lambda: datetime.now(UTC))
    accounts        = relationship("Account", back_populates="owner", cascade="all, delete-orphan")

class Account(Base):
    __tablename__ = "accounts"
    id         = Column(Integer, primary_key=True, index=True)
    number     = Column(String(20), unique=True, nullable=False, index=True)
    balance    = Column(Numeric(15, 2), default=Decimal("0.00"), nullable=False)
    is_active  = Column(Boolean, default=True, nullable=False)
    user_id    = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    owner        = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", foreign_keys="Transaction.account_id",
                                back_populates="account", cascade="all, delete-orphan")

class Transaction(Base):
    __tablename__ = "transactions"
    id                = Column(Integer, primary_key=True, index=True)
    type              = Column(Enum(TransactionType), nullable=False)
    amount            = Column(Numeric(15, 2), nullable=False)
    description       = Column(Text, nullable=True)
    account_id        = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    target_account_id = Column(Integer, ForeignKey("accounts.id", ondelete="SET NULL"), nullable=True)
    created_at        = Column(DateTime, default=lambda: datetime.now(UTC))
    account = relationship("Account", foreign_keys=[account_id], back_populates="transactions")
