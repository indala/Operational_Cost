from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from .database import engine, Base
from .routes import auth, users, expenses, predictions

# Initialize FastAPI
app = FastAPI(title="Operational Cost Prediction API")

# Create database tables
Base.metadata.create_all(bind=engine)

# Define base directory
BASE_DIR = Path(__file__).resolve().parent

# Setup Jinja2 template directory
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Mount static files (if any)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route (renders index.html using Jinja2)
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Admin dashboard route
@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    
    return templates.TemplateResponse("admin.html", {"request": request,"role": "admin"  })

@app.get("/faculty", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    
    return templates.TemplateResponse("user.html", {"request": request,"role": "faculty"  })



# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])
app.include_router(predictions.router, prefix="/predict", tags=["Prediction"])
