import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi import Request, Depends, status
from sqlalchemy import text

from auth import get_current_user_from_cookie
from database import SessionLocal, Base, engine
from auth import auth_router # Use the root auth.py for API endpoints
from routers.private import private_router
from routers.users import users_router
from routers.admin import admin_router
from routers.user_pages import router as user_router
from routers.api_users import router as api_users_router
from routers.kyc import kyc_router
from routers.cards import cards_router
from routers.deposits import deposits_router
from routers.loans import loans_router
from routers.investments import investments_router
from routers.realtime import realtime_router
from routers.account import router as account_router
from routers.financial_planning import router as financial_planning_router
from routers.insurance import router as insurance_router
from routers.notifications import router as notifications_router
from routers.settings import router as settings_router
from routers.support import router as support_router
from routers.projects import router as projects_router
from config import settings
from auth_utils import get_password_hash
from deps import get_current_user, get_current_admin_user

from models import User

async def create_db_and_tables():
    """Creates all database tables defined in models.py."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def test_db_connection():
    """Tests the database connection."""
    try:
        async with SessionLocal() as db:
            await db.execute(text("SELECT 1"))
            print("Database connection successful!")
            return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

async def create_admin_user():
    """Ensures the default admin user exists and is configured correctly."""
    from sqlalchemy import select
    async with SessionLocal() as db:
        result = await db.execute(select(User).filter(User.email == settings.ADMIN_EMAIL))
        admin_user = result.scalars().first()
        if not admin_user:
            # Create a new admin user with an argon2 hashed password if one doesn't exist
            hashed_password = get_password_hash(settings.ADMIN_PASSWORD)
            new_admin = User(
                full_name="Admin User",
                email=settings.ADMIN_EMAIL,
                hashed_password=hashed_password,
                is_admin=True,
                is_active=True
            )
            db.add(new_admin)
            await db.commit()
            print("Default admin user created successfully.")
        elif not admin_user.is_admin:
            # If admin user exists but is not marked as admin, update them.
            admin_user.is_admin = True
            await db.commit()
            print("Admin user existed but was not an admin. Updated successfully.")
        else:
            print("Admin user already exists.")




app = FastAPI()
origins = [
    "http://localhost:8000",  # FastAPI app
    "http://127.0.0.1:8000", # FastAPI app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def user_jail_middleware(request: Request, call_next):
    """
    This middleware enforces that authenticated users can only access routes
    under /user/, /api/, or /auth/logout.
    """
    # Paths that do not require this check
    # Add explicit signin/signup paths (and .html variants) so public auth pages aren't redirected
    exempt_paths = [
        "/api", "/auth", "/css", "/js", "/lib", "/img", "/static",
        "/docs", "/openapi.json", "/signin", "/signup", "/signin.html", "/signup.html", "/logout"
    ]
    is_exempt = any(request.url.path.startswith(p) for p in exempt_paths)
    
    if not is_exempt:
        user = await get_current_user_from_cookie(request)
        if user:
            # Ensure admin user is always marked as admin
            if user.email == settings.ADMIN_EMAIL and not user.is_admin:
                user.is_admin = True
            
            if not request.url.path.startswith("/user"):
                # If user is logged in and tries to access a public page like '/', redirect them to appropriate dashboard
                dashboard_url = "/user/admin/dashboard" if user.is_admin else "/user/dashboard"
                return RedirectResponse(url=dashboard_url)
            
    response = await call_next(request)
    return response


@app.on_event("startup")
async def startup_event():
    await create_db_and_tables()
    await test_db_connection()
    await create_admin_user()

# --- Static Files & Routers ---

# User-facing static assets (CSS, JS, Lib, Img)
app.mount("/css", StaticFiles(directory="static/css"), name="css")
app.mount("/js", StaticFiles(directory="static/js"), name="js")
app.mount("/lib", StaticFiles(directory="static/lib"), name="lib")
app.mount("/img", StaticFiles(directory="static/img"), name="img")
# Also mount the full `static` directory at `/static` to support templates
# that reference `/static/...` paths.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include API routers
app.include_router(auth_router, prefix="/auth")
app.include_router(private_router, prefix="/user") # Handles authenticated UI routes under /user/* and /user/admin/*
app.include_router(users_router, prefix="/api/v1/users")
app.include_router(admin_router, prefix="/api/admin")
app.include_router(api_users_router)  # /api/user/* endpoints
# Mount product routers under /api/v1 to serve JSON for user pages
app.include_router(kyc_router, prefix="/api/v1")
app.include_router(cards_router, prefix="/api/v1")
app.include_router(deposits_router, prefix="/api/v1")
app.include_router(loans_router, prefix="/api/v1")
app.include_router(investments_router, prefix="/api/v1")
# Account router (uploads, profile updates)
app.include_router(account_router, prefix="/api/v1")
# Feature routers
app.include_router(financial_planning_router)
app.include_router(insurance_router)
app.include_router(notifications_router)
app.include_router(settings_router)
app.include_router(support_router)
app.include_router(projects_router)
# Realtime WebSocket router
app.include_router(realtime_router)
# Include user-facing pages (prefix defined in router as /user)
app.include_router(user_router)

# --- Public Facing HTML Routes ---
@app.get("/signin")
async def signin_page(request: Request):
    return FileResponse("static/signin.html")

@app.get("/signup")
async def signup_page(request: Request):
    return FileResponse("static/signup.html")

@app.get("/logout")
async def logout_page(request: Request):
    """Logs out the user by clearing the access token cookie and redirecting to signin."""
    response = RedirectResponse(url="/signin", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="access_token", path="/")
    return response

# --- Static Files Mount ---
# This should be the LAST mount.
# The `html=True` argument makes it so that paths like "/" or "/about"
# will automatically serve "static/index.html" or "static/about.html".
app.mount("/", StaticFiles(directory="static", html=True), name="public")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)