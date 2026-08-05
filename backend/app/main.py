from fastapi import FastAPI
from app.api import router

app = FastAPI(title="MyoDiacker Decision Fusion API")
app.include_router(router)
