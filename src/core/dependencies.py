from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.portfolio.service import PortfolioService
from src.portfolio.repository import PortfolioRepository
from src.core.db import get_db
from src.core.mock import get_mock_user


def get_user():
    return get_mock_user()


def get_repo(session: AsyncSession = Depends(get_db)):
    return PortfolioRepository(session)


def get_service(repo: PortfolioRepository = Depends(get_repo)):
    return PortfolioService(repo)
    