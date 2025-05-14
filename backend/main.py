from fastapi import FastAPI

from backend.urls.auth import auth_router
from backend.urls.programs import router as programs_router

app = FastAPI()

app.include_router(router=programs_router)
app.include_router(router=auth_router)
