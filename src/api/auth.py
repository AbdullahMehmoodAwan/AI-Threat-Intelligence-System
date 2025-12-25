# src/api/auth.py

import os
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse

from passlib.context import CryptContext

router = APIRouter()

# ========= PASSWORD HASHING =========
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hard-coded admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = pwd.hash("admin")  # password = admin

# ========= TEMPLATE DIR =========
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # src/
TEMPLATE_DIR = os.path.join(BASE_DIR, "dashboard", "templates")

# ========= LOGIN PAGE =========
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return FileResponse(os.path.join(TEMPLATE_DIR, "login.html"))

# ========= LOGIN HANDLER =========
@router.post("/login")
async def login(request: Request,
                username: str = Form(...),
                password: str = Form(...)):

    # SUCCESS LOGIN
    if username == ADMIN_USERNAME and pwd.verify(password, ADMIN_PASSWORD_HASH):
        request.session["logged_in"] = True
        return RedirectResponse("/", status_code=302)

    # FAILED LOGIN → Show error message
    return RedirectResponse("/login?error=1", status_code=302)

# ========= LOGOUT =========
@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=302)
