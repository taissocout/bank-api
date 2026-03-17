from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas import AccountResponse, DepositRequest, WithdrawalRequest, TransferRequest, TransactionResponse
from services.account_service import (
    create_account, get_accounts, get_account, get_account_by_number,
    deposit, withdraw, transfer, get_history
)
from dependencies import get_current_user
from models import User

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.post("/", response_model=AccountResponse, status_code=201)
async def new_account(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await create_account(db, current_user.id)

@router.get("/", response_model=list[AccountResponse])
async def list_accounts(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await get_accounts(db, current_user.id)

@router.get("/{account_id}", response_model=AccountResponse)
async def account_detail(account_id: int, db: AsyncSession = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    return await get_account(db, account_id, current_user.id)

@router.post("/{account_id}/deposit", response_model=TransactionResponse)
async def do_deposit(account_id: int, data: DepositRequest, db: AsyncSession = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    account = await get_account(db, account_id, current_user.id)
    return await deposit(db, account, data.amount, data.description)

@router.post("/{account_id}/withdraw", response_model=TransactionResponse)
async def do_withdraw(account_id: int, data: WithdrawalRequest, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    account = await get_account(db, account_id, current_user.id)
    return await withdraw(db, account, data.amount, data.description)

@router.post("/{account_id}/transfer", response_model=TransactionResponse)
async def do_transfer(account_id: int, data: TransferRequest, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    origin = await get_account(db, account_id, current_user.id)
    target = await get_account_by_number(db, data.target_account_number)
    return await transfer(db, origin, target, data.amount, data.description)

@router.get("/{account_id}/history", response_model=list[TransactionResponse])
async def history(account_id: int, limit: int = 50, db: AsyncSession = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    await get_account(db, account_id, current_user.id)
    return await get_history(db, account_id, limit)
