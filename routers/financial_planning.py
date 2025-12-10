"""Financial Planning API endpoints for budgets and goals."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_current_user, SessionDep
from app.models import User
from crud import (
    create_budget,
    get_user_budgets,
    get_budget,
    update_budget,
    delete_budget,
    create_goal,
    get_user_goals,
    get_goal,
    update_goal,
    delete_goal,
)
from schemas import (
    Budget,
    BudgetCreate,
    Goal,
    GoalCreate,
)

router = APIRouter(
    prefix="/api/v1/financial",
    tags=["financial-planning"],
    dependencies=[Depends(get_current_user)]
)

# ===== BUDGETS =====

@router.post("/budgets", response_model=Budget)
async def create_budget_endpoint(
    budget: BudgetCreate,
    db_session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    """Create a new budget for the current user."""
    return await create_budget(db_session, budget, current_user.id)

@router.get("/budgets", response_model=List[Budget])
async def list_budgets(
    month: str = None,
    db_session: SessionDep = None,
    current_user: User = Depends(get_current_user),
):
    """Get all budgets for the current user, optionally filtered by month."""
    return await get_user_budgets(db_session, current_user.id, month)

@router.get("/budgets/{budget_id}", response_model=Budget)
async def get_budget_detail(
    budget_id: int,
    db_session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    """Get a specific budget."""
    budget = await get_budget(db_session, budget_id)
    if not budget or budget.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    return budget

@router.put("/budgets/{budget_id}", response_model=Budget)
async def update_budget_endpoint(
    budget_id: int,
    budget_data: dict,
    db_session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    """Update a budget."""
    budget = await get_budget(db_session, budget_id)
    if not budget or budget.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    return await update_budget(db_session, budget_id, budget_data)

@router.delete("/budgets/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_budget_endpoint(
    budget_id: int,
    db_session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    """Delete a budget."""
    budget = await get_budget(db_session, budget_id)
    if not budget or budget.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    await delete_budget(db_session, budget_id)

# ===== GOALS =====

@router.post("/goals", response_model=Goal)
async def create_goal_endpoint(
    goal: GoalCreate,
    db_session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    """Create a new financial goal."""
    return await create_goal(db_session, goal, current_user.id)

@router.get("/goals", response_model=List[Goal])
async def list_goals(
    skip: int = 0,
    limit: int = 100,
    db_session: SessionDep = None,
    current_user: User = Depends(get_current_user),
):
    """Get all financial goals for the current user."""
    return await get_user_goals(db_session, current_user.id, skip, limit)

@router.get("/goals/{goal_id}", response_model=Goal)
async def get_goal_detail(
    goal_id: int,
    db_session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    """Get a specific financial goal."""
    goal = await get_goal(db_session, goal_id)
    if not goal or goal.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return goal

@router.put("/goals/{goal_id}", response_model=Goal)
async def update_goal_endpoint(
    goal_id: int,
    goal_data: dict,
    db_session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    """Update a financial goal."""
    goal = await get_goal(db_session, goal_id)
    if not goal or goal.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return await update_goal(db_session, goal_id, goal_data)

@router.delete("/goals/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal_endpoint(
    goal_id: int,
    db_session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    """Delete a financial goal."""
    goal = await get_goal(db_session, goal_id)
    if not goal or goal.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    await delete_goal(db_session, goal_id)
