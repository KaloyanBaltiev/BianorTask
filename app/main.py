from fastapi import FastAPI
from core.database import Base

from core.database import engine
from api.endpoints.routers import router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
