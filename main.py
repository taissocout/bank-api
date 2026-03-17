import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config import get_settings
from database import init_db

settings = get_settings()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Bank API [{settings.app_env}]")
    if not settings.is_production:
        await init_db()
    yield

app = FastAPI(
    title=settings.app_title, version=settings.app_version,
    description="API Bancaria Assincrona - DIO Desafio 2026",
    docs_url=None if settings.is_production else "/docs",
    redoc_url=None if settings.is_production else "/redoc",
    openapi_url=None if settings.is_production else "/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(CORSMiddleware, allow_origins=settings.origins_list,
                   allow_credentials=True, allow_methods=["GET","POST","PUT","DELETE"],
                   allow_headers=["Content-Type","Authorization"])

@app.exception_handler(Exception)
async def global_exc(request: Request, exc: Exception):
    logger.exception(f"Erro: {request.method} {request.url.path}")
    return JSONResponse(status_code=500, content={"detail": "Erro interno."})

@app.get("/", tags=["health"])
async def root():
    return {"status": "ok", "app": settings.app_title, "version": settings.app_version}

@app.get("/health", tags=["health"])
async def health():
    return {"status": "healthy", "db": "postgresql" if settings.is_postgres else "sqlite"}

from routers.auth import router as auth_router
from routers.accounts import router as accounts_router
app.include_router(auth_router)
app.include_router(accounts_router)
