import random, string
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from models import Account, Transaction, TransactionType

def _gen_number(): return "".join(random.choices(string.digits, k=10))

async def create_account(db: AsyncSession, user_id: int) -> Account:
    for _ in range(10):
        n = _gen_number()
        if not (await db.execute(select(Account).where(Account.number == n))).scalars().first(): break
    acc = Account(number=n, user_id=user_id)
    db.add(acc); await db.flush(); await db.refresh(acc)
    return acc

async def get_accounts(db: AsyncSession, user_id: int):
    r = await db.execute(select(Account).where(Account.user_id == user_id))
    return r.scalars().all()

async def get_account(db: AsyncSession, account_id: int, user_id: int) -> Account:
    r = await db.execute(select(Account).where(Account.id == account_id, Account.user_id == user_id))
    acc = r.scalars().first()
    if not acc: raise HTTPException(404, "Conta nao encontrada")
    return acc

async def get_account_by_number(db: AsyncSession, number: str) -> Account:
    r = await db.execute(select(Account).where(Account.number == number))
    acc = r.scalars().first()
    if not acc: raise HTTPException(404, "Conta destino nao encontrada")
    return acc

async def deposit(db: AsyncSession, account: Account, amount: Decimal, desc) -> Transaction:
    account.balance = Decimal(str(account.balance)) + amount
    tx = Transaction(type=TransactionType.DEPOSIT, amount=amount, description=desc, account_id=account.id)
    db.add(tx); await db.flush(); await db.refresh(tx)
    return tx

async def withdraw(db: AsyncSession, account: Account, amount: Decimal, desc) -> Transaction:
    balance = Decimal(str(account.balance))
    if balance < amount:
        raise HTTPException(422, f"Saldo insuficiente. Saldo: {balance}, Solicitado: {amount}")
    account.balance = balance - amount
    tx = Transaction(type=TransactionType.WITHDRAWAL, amount=amount, description=desc, account_id=account.id)
    db.add(tx); await db.flush(); await db.refresh(tx)
    return tx

async def transfer(db: AsyncSession, origin: Account, target: Account, amount: Decimal, desc) -> Transaction:
    if origin.id == target.id: raise HTTPException(422, "Conta origem e destino sao iguais")
    balance = Decimal(str(origin.balance))
    if balance < amount:
        raise HTTPException(422, f"Saldo insuficiente. Saldo: {balance}, Solicitado: {amount}")
    origin.balance = balance - amount
    target.balance = Decimal(str(target.balance)) + amount
    tx = Transaction(type=TransactionType.TRANSFER, amount=amount, description=desc,
                     account_id=origin.id, target_account_id=target.id)
    db.add(tx); await db.flush(); await db.refresh(tx)
    return tx

async def get_history(db: AsyncSession, account_id: int, limit: int = 50):
    r = await db.execute(
        select(Transaction).where(Transaction.account_id == account_id)
        .order_by(Transaction.created_at.desc()).limit(limit)
    )
    return r.scalars().all()
