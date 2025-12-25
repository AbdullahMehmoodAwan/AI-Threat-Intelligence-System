# src/api/server.py

import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from src.api.schemas import LogInput, FusionOutput
from src.nlp_engine.fusion_engine import fusion_engine
from src.database.history import save_history, load_history
from src.api.auth import router as auth_router
from src.api.export import router as export_router

# ----------------------------------------------------
# APP INITIALIZATION
# ----------------------------------------------------

app = FastAPI()

# Sessions for login
app.add_middleware(SessionMiddleware, secret_key="supersecretkey123")

# Include routers FIRST
app.include_router(auth_router)
app.include_router(export_router)

# ----------------------------------------------------
# PATHS
# ----------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # src/
DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboard", "templates")

# Serve static files
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "dashboard", "static")),
    name="static"
)

# ----------------------------------------------------
# LOGIN CHECK
# ----------------------------------------------------

def protected(request: Request):
    if not request.session.get("logged_in"):
        return RedirectResponse("/login", status_code=302)
    return None

# ----------------------------------------------------
# ROUTES
# ----------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    check = protected(request)
    if check:
        return check
    return FileResponse(os.path.join(DASHBOARD_DIR, "index.html"))

@app.get("/dashboard/", response_class=HTMLResponse)
def dashboard_page(request: Request):
    check = protected(request)
    if check:
        return check
    return FileResponse(os.path.join(DASHBOARD_DIR, "index.html"))

@app.get("/history", response_class=HTMLResponse)
def history_page(request: Request):
    check = protected(request)
    if check:
        return check
    return FileResponse(os.path.join(DASHBOARD_DIR, "history.html"))

@app.get("/api/history")
def history_api(request: Request):
    check = protected(request)
    if check:
        return check
    return JSONResponse(load_history())

@app.get("/analytics", response_class=HTMLResponse)
def analytics_page(request: Request):
    check = protected(request)
    if check:
        return check
    return FileResponse(os.path.join(DASHBOARD_DIR, "analytics.html"))


@app.post("/fusion", response_model=FusionOutput)
def fusion_endpoint(request: Request, input: LogInput):
    check = protected(request)
    if check:
        return check

    output = fusion_engine(input.text)

    save_history({
        "input": input.text,
        "threat_type": output["threat_type"],
        "iocs": output["iocs"],
        "summary": output["summary"],
        "anomaly_score": output["anomaly_score"]
    })

    return output
