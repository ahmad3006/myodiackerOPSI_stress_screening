from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router

app = FastAPI(title="MyoDiacker Decision Fusion API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
