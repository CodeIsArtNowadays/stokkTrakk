from fastapi import APIRouter, Depends

from src.core.dependencies import get_user, get_service
from src.auth.models import User
from src.portfolio.service import PortfolioService
from src.portfolio.schemas import (
    TransactionCreateRequestSchema,
    CoinCreateSchema,
    TransactionRetrieveSchema
)


api_router = APIRouter() # testing
    

@api_router.get('/txs', response_model=list[TransactionRetrieveSchema])
async def get_user_txs(
    user: User = Depends(get_user),
    service: PortfolioService = Depends(get_service)
):
    return await service.get_all_user_tx(user.id)
    

@api_router.post('/txs', response_model=TransactionRetrieveSchema)
async def create_tx(
    tx_data: TransactionCreateRequestSchema,
    user: User = Depends(get_user),
    service: PortfolioService = Depends(get_service)
):
    return await service.create_tx(tx_data, user.id)
    

@api_router.post('/coins')
async def create_coin(coin_data: CoinCreateSchema, service: PortfolioService = Depends(get_service)):
    return await service.create_coin(coin_data)
    
    
@api_router.get('/search')
async def search_coins(q: str, service: PortfolioService = Depends(get_service)):
    return await service.search_coins(q)