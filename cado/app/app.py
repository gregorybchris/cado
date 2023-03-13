from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cado.app import routes

ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

app = FastAPI()

app.include_router(routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)