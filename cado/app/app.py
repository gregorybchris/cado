from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from cado.app import routes

ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

app = FastAPI()

app.include_router(routes.router)

app.mount("/abc", StaticFiles(directory=Path(__file__).resolve().parent / "static", html=True), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
