"""User API endpoints for fetching and managing user-specific financial data."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_current_user, SessionDep
from app.models import User
from crud import (
    get_user, 
    get_user_transactions,
    get_user_deposits,
    get_user_loans,
    get_user_investments,
    get_user_cards
)
from schemas import (
    User as PydanticUser,
    Transaction as PydanticTransaction,
    Deposit as PydanticDeposit,
    Loan as PydanticLoan,
    Investment as PydanticInvestment,
    Card as PydanticCard,
    Account as PydanticAccount
)

router = APIRouter(
    prefix="/api/user",
    tags=["user-api"],
    dependencies=[Depends(get_current_user)]
)


# USER PROFILE & ACCOUNT INFO
@router.get("/profile", response_model=PydanticUser)
async def get_user_profile(
    current_user: User = Depends(get_current_user),
):
    """Get current user's profile information."""
    return current_user


@router.get("/dashboard", response_model=dict)
async def get_user_dashboard_data(
    db_session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    """Get dashboard summary data (balance, investments, loans, recent transactions)."""
    try:
        # Get user with all relations
        user = await get_user(db_session, current_user.id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get recent transactions
        transactions = await get_user_transactions(db_session, user.id, skip=0, limit=5)
        
        # Get deposits, loans, investments
        deposits = await get_user_deposits(db_session, user.id)
        loans = await get_user_loans(db_session, user.id)
        investments = await get_user_investments(db_session, user.id)
        
        # Calculate summary metrics
        total_balance = sum(d.amount for d in deposits) if deposits else 0.0
        active_investments = len([i for i in investments if i.status == "active"]) if investments else 0
        active_loans = len([l for l in loans if l.status == "active"]) if loans else 0
        
        return {
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "account_number": user.account_number
            },
            "balance": total_balance,
            "active_investments": active_investments,
            "active_loans": active_loans,
            "recent_transactions": [
                {
                    "id": t.id,
                    "amount": t.amount,
                    "type": t.transaction_type,
                    "status": t.status,
                    "created_at": t.created_at.isoformat() if t.created_at else None
                }
                for t in transactions
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# TRANSACTIONS
@router.get("/transactions", response_model=List[PydanticTransaction])
async def get_user_txn_list(
    db_session: SessionDep,
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """Get user's transactions."""
    transactions = await get_user_transactions(db_session, current_user.id, skip=skip, limit=limit)
    return transactions


# CARDS
@router.get("/cards", response_model=List[PydanticCard])
async def get_user_cards_list(
    db_session: SessionDep,
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """Get user's cards."""
    cards = await get_user_cards(db_session, current_user.id, skip=skip, limit=limit)
    return cards


@router.get("/cards/{card_id}", response_model=PydanticCard)
async def get_user_card_detail(
    card_id: int,
    db_session: SessionDep,
    current_user: User = Depends(get_current_user)
):
    """Get a specific card."""
    from crud import get_card
    card = await get_card(db_session, card_id)
    if not card or card.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Card not found")
    return card


# DEPOSITS
@router.get("/deposits", response_model=List[PydanticDeposit])
async def get_user_deposits_list(
    db_session: SessionDep,
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """Get user's deposits."""
    deposits = await get_user_deposits(db_session, current_user.id, skip=skip, limit=limit)
    return deposits


@router.get("/deposits/{deposit_id}", response_model=PydanticDeposit)
async def get_user_deposit_detail(
    deposit_id: int,
    db_session: SessionDep,
    current_user: User = Depends(get_current_user)
):
    """Get a specific deposit."""
    from crud import get_deposit
    deposit = await get_deposit(db_session, deposit_id)
    if not deposit or deposit.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Deposit not found")
    return deposit


# LOANS
@router.get("/loans", response_model=List[PydanticLoan])
async def get_user_loans_list(
    db_session: SessionDep,
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """Get user's loans."""
    loans = await get_user_loans(db_session, current_user.id, skip=skip, limit=limit)
    return loans


@router.get("/loans/{loan_id}", response_model=PydanticLoan)
async def get_user_loan_detail(
    loan_id: int,
    db_session: SessionDep,
    current_user: User = Depends(get_current_user)
):
    """Get a specific loan."""
    from crud import get_loan
    loan = await get_loan(db_session, loan_id)
    if not loan or loan.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan


# INVESTMENTS
@router.get("/investments", response_model=List[PydanticInvestment])
async def get_user_investments_list(
    db_session: SessionDep,
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """Get user's investments."""
    investments = await get_user_investments(db_session, current_user.id, skip=skip, limit=limit)
    return investments


@router.get("/investments/{investment_id}", response_model=PydanticInvestment)
async def get_user_investment_detail(
    investment_id: int,
    db_session: SessionDep,
    current_user: User = Depends(get_current_user)
):
    """Get a specific investment."""
    from crud import get_investment
    investment = await get_investment(db_session, investment_id)
    if not investment or investment.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Investment not found")
    return investment
