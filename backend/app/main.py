from fastapi import FastAPI

from app.core.config import get_settings
from app.core.cors import setup_cors
from app.routers.public import router as public_router

settings = get_settings()
app = FastAPI(title=settings.app_name)
setup_cors(app)
app.include_router(public_router)


@app.get('/health')
def health() -> dict[str, str]:
    return {'status': 'ok'}
