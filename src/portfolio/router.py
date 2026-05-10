from fastapi import APIRouter, Depends

from src.core.dependencies import get_user, get_service
from src.auth.models import User
from src.portfolio.service import PortfolioService
from src.portfolio.schemas import (
    TransactionCreateRequestSchema,
    TransactionCreateSchema,
    CoinCreateSchema
)


api_router = APIRouter() # testing


@api_router.get('/')
async def index(service: PortfolioService = Depends(get_service)):
    await service.get_price_by_symbol('asd') # testing
    

@api_router.get('/txs')
async def get_user_txs(
    user: User = Depends(get_user),
    service: PortfolioService = Depends(get_service)
):
    return await service.get_all_user_tx(user.id)
    

@api_router.post('/txs')
async def create_tx(
    tx_data: TransactionCreateRequestSchema,
    user: User = Depends(get_user),
    service: PortfolioService = Depends(get_service)
):
    tx_updated_data = TransactionCreateSchema(**tx_data.model_dump(), user_id=user.id)
    return await service.create_tx(tx_updated_data)
    

@api_router.post('/coins')
async def create_coin(coin_data: CoinCreateSchema, service: PortfolioService = Depends(get_service)):
    return await service.create_coin(coin_data)
    
    
@api_router.get('/search')
async def search_coins(q: str, service: PortfolioService = Depends(get_service)):
    return await service.search_coins(q)