# schemas.py
# Pydantic models for request/response validation and serialization.

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str
    is_admin: bool
    user_id: int
    email: str
    full_name: Optional[str] = None

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None

class User(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    account_number: Optional[str] = None
    account_type: Optional[str] = None
    is_admin: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AccountBase(BaseModel):
    account_number: str
    balance: float
    currency: str

class AccountCreate(AccountBase):
    pass

class Account(AccountBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    amount: float
    transaction_type: str
    status: str

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    user_id: int
    account_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class KYCInfoBase(BaseModel):
    document_type: str
    document_number: str
    status: str

class KYCInfoCreate(KYCInfoBase):
    pass

class KYCInfo(KYCInfoBase):
    id: int
    user_id: int
    submitted_at: datetime
    approved_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class FormSubmissionBase(BaseModel):
    form_type: str
    data: str # Can be a dict if you use a JSON type in the DB

class FormSubmissionCreate(FormSubmissionBase):
    pass

class FormSubmission(FormSubmissionBase):
    id: int
    user_id: Optional[int] = None
    submitted_at: datetime

    class Config:
        from_attributes = True


class KYCSubmissionBase(BaseModel):
    document_type: str
    document_file_path: str
    status: str = "pending"


class KYCSubmissionCreate(KYCSubmissionBase):
    pass


class KYCSubmission(KYCSubmissionBase):
    id: int
    user_id: int
    submitted_at: datetime
    reviewed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Schemas for Deposits
class DepositBase(BaseModel):
    amount: float
    currency: str
    status: str = "completed"

class DepositCreate(DepositBase):
    pass

class Deposit(DepositBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Schemas for Loans
class LoanBase(BaseModel):
    amount: float
    interest_rate: float
    term_months: int
    status: str = "active"

class LoanCreate(LoanBase):
    pass

class Loan(LoanBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Schemas for Investments
class InvestmentBase(BaseModel):
    investment_type: str
    amount: float
    status: str = "active"

class InvestmentCreate(InvestmentBase):
    pass

class Investment(InvestmentBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Schemas for Cards
class CardBase(BaseModel):
    card_number: str
    card_type: str
    expiry_date: str
    status: str = "active"

class CardCreate(CardBase):
    pass

class Card(CardBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Schemas for Policies
class PolicyBase(BaseModel):
    policy_number: str
    policy_type: str
    coverage_amount: float
    premium: float
    start_date: datetime
    renewal_date: datetime
    status: str = "active"

class PolicyCreate(PolicyBase):
    pass

class Policy(PolicyBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Schemas for Claims
class ClaimBase(BaseModel):
    claim_number: str
    amount: float
    status: str = "pending"
    description: str

class ClaimCreate(ClaimBase):
    pass

class Claim(ClaimBase):
    id: int
    policy_id: int
    submitted_at: datetime
    reviewed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Schemas for Budgets
class BudgetBase(BaseModel):
    category: str
    limit: float
    spent: float = 0.0
    month: str

class BudgetCreate(BudgetBase):
    pass

class Budget(BudgetBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Schemas for Goals
class GoalBase(BaseModel):
    goal_name: str
    target_amount: float
    current_amount: float = 0.0
    deadline: datetime
    status: str = "active"

class GoalCreate(GoalBase):
    pass

class Goal(GoalBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Schemas for Notifications
class NotificationBase(BaseModel):
    title: str
    message: str
    notification_type: str
    is_read: bool = False

class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Schemas for Support Tickets
class SupportTicketBase(BaseModel):
    subject: str
    message: str
    priority: str = "normal"

class SupportTicketCreate(SupportTicketBase):
    pass

class SupportTicket(SupportTicketBase):
    id: int
    ticket_number: str
    user_id: Optional[int] = None
    status: str = "open"
    created_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Schemas for User Settings
class UserSettingsBase(BaseModel):
    two_factor_enabled: bool = False
    email_notifications: bool = True
    sms_notifications: bool = False
    phone_number: Optional[str] = None
    address: Optional[str] = None
    preferences: Optional[str] = None

class UserSettingsCreate(UserSettingsBase):
    pass

class UserSettings(UserSettingsBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schemas for Projects
class ProjectBase(BaseModel):
    project_name: str
    description: str
    status: str = "planning"
    budget: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class AdminDashboardMetrics(BaseModel):
    total_users: int
    total_transactions: int
    total_volume: float

    class Config:
        from_attributes = True

class FundUserRequest(BaseModel):
    amount: float
    currency: str = "USD"
    description: Optional[str] = None
    reference_number: Optional[str] = None

class FundUserResponse(BaseModel):
    status: str
    message: str
    new_balance: float

class AdjustBalanceRequest(BaseModel):
    amount: float
    currency: str = "USD"
    description: Optional[str] = None
    operation_type: str = "credit"

class CreateAccountRequest(BaseModel):
    account_number: Optional[str] = None
    currency: str = "USD"
    account_type: str = "savings"  # savings, checking, business
    initial_balance: float = 0.0

class KYCApprovalRequest(BaseModel):
    notes: Optional[str] = None

class KYCRejectionRequest(BaseModel):
    notes: Optional[str] = None