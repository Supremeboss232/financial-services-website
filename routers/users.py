from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from auth_utils import create_access_token
from deps import CurrentUserDep, SessionDep, validate_password_length
from schemas import User as PydanticUser, UserCreate
from crud import get_user, get_users, create_user, get_user_by_username
from typing import Annotated

users_router = APIRouter(prefix="/users", tags=["users"])

@users_router.post("/", response_model=PydanticUser, status_code=status.HTTP_201_CREATED)
async def create_new_user(
    user: UserCreate,
    db_session: SessionDep,
    validated_password: str = Depends(validate_password_length) # Add password validation
):
    db_user = await get_user_by_username(db_session, username=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    new_user = await create_user(db=db_session, user=user)
    # Return the created user object directly to match the response_model
    return new_user

@users_router.get("/me/", response_model=PydanticUser)
async def read_users_me(current_user: CurrentUserDep):
    return current_user

@users_router.get("/{user_id}", response_model=PydanticUser)
async def read_user(user_id: int, db_session: SessionDep):
    db_user = await get_user(db_session, user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@users_router.get("/", response_model=List[PydanticUser])
async def read_all_users(db_session: SessionDep, skip: int = 0, limit: int = 100, current_user: CurrentUserDep = None):
    # This endpoint would typically be admin-only or require specific permissions
    # For now, it's accessible to any logged-in user.
    # Consider adding admin-specific dependency here: Depends(get_current_admin_user)
    users = await get_users(db_session, skip=skip, limit=limit)
    return users

@users_router.get("/me/stats")
async def read_user_stats(current_user: CurrentUserDep, db_session: SessionDep):
    """Returns user-specific statistics: balance, investments, loans, transactions."""
    from crud import get_user_deposits, get_user_investments, get_user_loans, get_user_transactions
    
    deposits = await get_user_deposits(db_session, current_user.id, limit=100)
    investments = await get_user_investments(db_session, current_user.id, limit=100)
    loans = await get_user_loans(db_session, current_user.id, limit=100)
    transactions = await get_user_transactions(db_session, current_user.id, limit=50)
    
    total_balance = sum(d.amount for d in deposits if d.amount) if deposits else 0
    total_investments = sum(i.amount for i in investments if i.amount) if investments else 0
    total_loans = sum(l.amount for l in loans if l.amount) if loans else 0
    
    return {
        "user": current_user,
        "balance": total_balance,
        "investments": total_investments,
        "loans": total_loans,
        "recent_transactions": transactions[:10],
        "deposits_count": len(deposits),
        "investments_count": len(investments),
        "loans_count": len(loans),
        "is_verified": getattr(current_user, "is_verified", False),
        "account_number": getattr(current_user, "account_number", None)
    }
