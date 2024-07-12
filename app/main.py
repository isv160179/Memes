from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi_pagination.utils import disable_installed_extensions_check

from app.api.routers import main_router
from app.core.config import settings

app = FastAPI(title=settings.app_title, description=settings.app_description)
app.include_router(main_router)
add_pagination(app)
disable_installed_extensions_check()