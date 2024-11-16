from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from time import sleep

from fastapi import FastAPI

from alembic import command
from alembic.config import Config
from src.common.logger import logger
from src.common.settings import settings
from src.delivery.api.v1.users.users_router import users_router


def run_sql_migrations() -> None:
    logger.info("Running SQL migrations...")

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    logger.info("SQL migrations finished!")


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator:
    logger.info("Starting FastAPI server...")
    run_sql_migrations()

    yield

    # Graceful shutdown
    sleep(5)  # wait for the app to finish processing requests
    logger.info("FastAPI server finished!")


app = FastAPI(
    title=settings.project_name,
    description=settings.description,
    lifespan=lifespan,
    openapi_url=settings.openapi_url,
)

app.include_router(prefix=settings.api_v1_prefix, router=users_router)
