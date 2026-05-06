from fastapi import APIRouter

from src.portfolio.service import portfolio_service # testing

api_router = APIRouter() # testing


@api_router.get('/')
async def index():
    await portfolio_service.get_price_by_symbol('asd') # testing