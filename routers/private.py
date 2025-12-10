from fastapi import APIRouter, Request, Depends, status, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import selectinload
from pathlib import Path

from models import User
from deps import get_current_user, get_current_admin_user

# --- Path Setup ---
BASE_PATH = Path(__file__).resolve().parent.parent

private_router = APIRouter(
    tags=["Private UI"],
    # Dependencies that apply to all routes in this router
    dependencies=[Depends(get_current_user)]
)

# --- Template Configuration ---
user_templates = Jinja2Templates(directory=str(BASE_PATH / "private/user"))
admin_templates = Jinja2Templates(directory=str(BASE_PATH / "private/admin"))


# --- Authenticated User-Facing UI Routes ---

@private_router.get("/dashboard")
async def dashboard(request: Request, current_user: User = Depends(get_current_user)):
    """Renders the user's main dashboard with data from the database."""
    # In a real app, you'd fetch more complex user-specific data from other tables.
    # The relationships (accounts, investments, loans) are now eagerly loaded via the dependency.
    
    total_balance = sum(account.balance for account in current_user.accounts)
    total_investments = sum(investment.amount for investment in current_user.investments)
    total_loans = sum(loan.amount for loan in current_user.loans)

    user_data = {
        "username": current_user.full_name or current_user.email,
        "balance": total_balance,
        "investments_value": total_investments,
        "outstanding_loans": total_loans
    }
    # Include verification and account info so templates can show KYC state
    user_data["is_verified"] = getattr(current_user, "is_verified", False)
    user_data["account_number"] = getattr(current_user, "account_number", None)
    return user_templates.TemplateResponse("dashboard.html", {"request": request, "user": user_data})

@private_router.get("/cards")
async def cards_page(request: Request, current_user: User = Depends(get_current_user)):
    """Renders the user's cards page."""
    return user_templates.TemplateResponse("cards.html", {"request": request, "user": current_user})

@private_router.get("/investments")
async def investments_page(request: Request, current_user: User = Depends(get_current_user)):
    """Renders the user's investments page."""
    return user_templates.TemplateResponse("investments.html", {"request": request, "user": current_user})

@private_router.get("/loans")
async def loans_page(request: Request, current_user: User = Depends(get_current_user)):
    """Renders the user's loans page."""
    return user_templates.TemplateResponse("loans.html", {"request": request, "user": current_user})

@private_router.get("/insurance")
async def insurance_page(request: Request, current_user: User = Depends(get_current_user)):
    """Renders the user's insurance page."""
    return user_templates.TemplateResponse("insurance.html", {"request": request, "user": current_user})

@private_router.get("/deposits")
async def deposits_page(request: Request, current_user: User = Depends(get_current_user)):
    """Renders the user's deposits page."""
    return user_templates.TemplateResponse("deposits.html", {"request": request, "user": current_user})


@private_router.get("/kyc/verify")
async def kyc_verify_page(request: Request, current_user: User = Depends(get_current_user)):
    """Renders the KYC submission form for the current user."""
    return user_templates.TemplateResponse("kyc_form.html", {"request": request, "user": current_user})

@private_router.get("/kyc_form")
async def kyc_form_page(request: Request, current_user: User = Depends(get_current_user)):
    """Renders the KYC submission form (alternate route from /user/kyc_form)."""
    return user_templates.TemplateResponse("kyc_form.html", {"request": request, "user": current_user})

@private_router.get("/kyc_pending")
async def kyc_pending_page(request: Request, current_user: User = Depends(get_current_user)):
    """Renders the KYC pending status page."""
    return user_templates.TemplateResponse("kyc_pending.html", {"request": request, "user": current_user})

@private_router.get("/kyc_rejected")
async def kyc_rejected_page(request: Request, current_user: User = Depends(get_current_user)):
    """Renders the KYC rejection page."""
    return user_templates.TemplateResponse("kyc_rejected.html", {"request": request, "user": current_user})

@private_router.get("/kyc_success")
async def kyc_success_page(request: Request, current_user: User = Depends(get_current_user)):
    """Renders the KYC success/approved page."""
    return user_templates.TemplateResponse("kyc_success.html", {"request": request, "user": current_user})

@private_router.get("/profile")
async def profile_page(request: Request, current_user: User = Depends(get_current_user)):
    """Renders the user's profile page."""
    return user_templates.TemplateResponse("profile.html", {"request": request, "user": current_user})

@private_router.get("/account")
async def account_settings_page(request: Request, current_user: User = Depends(get_current_user)):
    """Renders the user's account settings page."""
    return user_templates.TemplateResponse("account.html", {"request": request, "user": current_user})

@private_router.get("/admin/dashboard", tags=["Admin UI"])
async def admin_dashboard(request: Request, current_user: User = Depends(get_current_admin_user)):
    """Renders the admin dashboard."""
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return admin_templates.TemplateResponse("admin_dashboard.html", {"request": request, "user": current_user})

@private_router.get("/admin/admin_users.html", tags=["Admin UI"])
async def admin_users_page(request: Request, current_user: User = Depends(get_current_admin_user)):
    return admin_templates.TemplateResponse("admin_users.html", {"request": request, "user": current_user})

@private_router.get("/admin/profile", tags=["Admin UI"])
async def admin_profile_page(request: Request, current_user: User = Depends(get_current_admin_user)):
    return admin_templates.TemplateResponse("admin_profile.html", {"request": request, "user": current_user})

@private_router.get("/admin/settings", tags=["Admin UI"])
async def admin_settings_page(request: Request, current_user: User = Depends(get_current_admin_user)):
    return admin_templates.TemplateResponse("admin_settings.html", {"request": request, "user": current_user})

@private_router.get("/admin/reports", tags=["Admin UI"])
async def admin_reports_page(request: Request, current_user: User = Depends(get_current_admin_user)):
    return admin_templates.TemplateResponse("admin_reports.html", {"request": request, "user": current_user})

@private_router.get("/admin/submissions", tags=["Admin UI"])
async def admin_submissions_page(request: Request, current_user: User = Depends(get_current_admin_user)):
    return admin_templates.TemplateResponse("admin_submissions.html", {"request": request, "user": current_user})

@private_router.get("/admin/kyc", tags=["Admin UI"])
async def admin_kyc_page(request: Request, current_user: User = Depends(get_current_admin_user)):
    return admin_templates.TemplateResponse("admin_kyc.html", {"request": request, "user": current_user})

@private_router.get("/admin/{page}", tags=["Admin UI"])
async def admin_generic_page(page: str, request: Request, current_user: User = Depends(get_current_admin_user)):
    """Serve admin templates dynamically.

    Maps requests like `/admin/transactions` -> `private/admin/admin_transactions.html`.
    If the template doesn't exist, return a 404.
    
    Note: /admin/dashboard is handled by the dedicated route above.
    """
    from jinja2 import TemplateNotFound
    
    # Skip dashboard - it's handled by the dedicated route
    if page == "dashboard":
        raise HTTPException(status_code=404, detail="Admin page 'dashboard' not found")
    
    # Normalize requested page to a template filename
    template_name = page if page.endswith('.html') else f"admin_{page}.html"
    try:
        return admin_templates.TemplateResponse(template_name, {"request": request, "user": current_user})
    except TemplateNotFound:
        raise HTTPException(status_code=404, detail=f"Admin page '{page}' not found")

@private_router.get("/logout")
async def logout(request: Request):
    """
    Logs out the user by clearing the access token cookie and redirecting to the sign-in page.
    """
    # Redirect to the sign-in page. The frontend will receive this and should act on it.
    response = RedirectResponse(url="/signin", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="access_token", path="/")
    return response