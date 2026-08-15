from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.init_db import init_db

from app.api import auth
from app.api import content
from app.api import recommendation
from app.api import interaction
from app.api import search
from app.api import profile
from app.api import focus


app = FastAPI(
    title="Multimodal Recommendation API",
    version="1.0.0"
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# ---------------------------------------------------------
# Database initialization
# ---------------------------------------------------------

@app.on_event("startup")
def startup():

    init_db()


# ---------------------------------------------------------
# Routers
# ---------------------------------------------------------

app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

app.include_router(
    content.router
)

app.include_router(
    recommendation.router
)

app.include_router(
    search.router,
    tags=["Semantic Search"]
)

app.include_router(
    interaction.router,
    tags=["Interactions"]
)

app.include_router(
    profile.router,
    tags=["Profile"]
)

app.include_router(
    focus.router,
    tags=["Focus Sessions"]
)


# ---------------------------------------------------------
# Home
# ---------------------------------------------------------

@app.get("/")
def home():

    return {
        "message":
        "Welcome to the Multimodal Recommendation API"
    }