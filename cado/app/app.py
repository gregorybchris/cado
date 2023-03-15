from pathlib import Path
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from cado.app import routes

ALLOWED_ORIGINS: List[str] = []

app = FastAPI()

app.include_router(routes.router)

static_dirpath = Path(__file__).resolve().parent.parent / "ui" / "dist"
app.mount("/", StaticFiles(directory=static_dirpath, html=True), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
