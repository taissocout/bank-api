from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator
from models import TransactionType

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class UserResponse(BaseModel):
    id: int; username: str; email: str; is_active: bool; created_at: datetime
    model_config = {"from_attributes": True}

class LoginRequest(BaseModel):
    username: str; password: str

class TokenResponse(BaseModel):
    access_token: str; token_type: str = "bearer"

class AccountResponse(BaseModel):
    id: int; number: str; balance: Decimal; is_active: bool; created_at: datetime
    model_config = {"from_attributes": True}

class DepositRequest(BaseModel):
    amount: Decimal = Field(gt=0); description: str | None = Field(None, max_length=255)

class WithdrawalRequest(BaseModel):
    amount: Decimal = Field(gt=0); description: str | None = Field(None, max_length=255)

class TransferRequest(BaseModel):
    target_account_number: str
    amount: Decimal = Field(gt=0); description: str | None = Field(None, max_length=255)
    @field_validator("amount")
    @classmethod
    def positive(cls, v):
        if v <= 0: raise ValueError("Valor deve ser positivo")
        return v

class TransactionResponse(BaseModel):
    id: int; type: TransactionType; amount: Decimal; description: str | None
    account_id: int; target_account_id: int | None; created_at: datetime
    model_config = {"from_attributes": True}
