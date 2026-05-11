from decimal import Decimal

from aiohttp import ClientSession

from src.core.exceptions import ExternalAPIError
from src.portfolio.models import Coin as CoinModel
from src.portfolio.models import Transaction as TransactionModel
from src.portfolio.repository import PortfolioRepository
from config import settings
from src.portfolio.schemas import (
    CoinCreateSchema,
    TransactionCreateRequestSchema,
    TransactionCreateSchema,
)


class PortfolioService:
    def __init__(self, repo: PortfolioRepository): 
        self.repo = repo
        self.params = {"x-cg-demo-api-key": settings.COINGECKO_API_KEY}
        self.base_url = 'https://api.coingecko.com/api/v3'
        
    async def search_coins(self, query):
        url = self.base_url + f"/search?query={query}"
        
        async with ClientSession() as session:
            async with session.get(url, params=self.params) as resp:
                
                if resp.status != 200:
                    raise ExternalAPIError(f'CoinGecko Error: {resp.status}')
                    
                data = await resp.json()
                res = [
                    {k: v for k, v in coin.items() if k in ['id', 'name', 'symbol']} for coin in data['coins']
                ]
                
                return res
                
    async def get_price_by_cg_id(self, cg_id: str):
        url = self.base_url + f'/simple/price?ids={cg_id}&vs_currencies=usd'
        
        async with ClientSession() as session:
            async with session.get(url, params=self.params) as resp:
                
                if resp.status != 200:
                    raise ExternalAPIError(f'CoinGecko Error: {resp.status}')
                    
                data = await resp.json()
                return Decimal(str((data[cg_id]['usd'])))
    
    async def get_coin_data_by_cg_id(self, cg_id: str) -> CoinCreateSchema:
        
        async with ClientSession() as session:
            url = self.base_url + f'/coins/{cg_id}'
            async with session.get(url, params=self.params) as resp:
                if resp.status != 200:
                    raise ExternalAPIError(f'CoinGecko Error: {resp.status}')
                    
                data = await resp.json()
                return CoinCreateSchema(title=data['name'], symbol=data['symbol'], cg_id=cg_id)
      
    async def create_coin(self, coin_data: CoinCreateSchema):
        return await self.repo.create_coin(coin_data)
        
    async def get_or_create_coin(self, cg_id: str) -> CoinModel:
        
        coin = await self.repo.get_coin_by_cg_id(cg_id)
        if not coin:
            coin_data = await self.get_coin_data_by_cg_id(cg_id)
            coin = await self.create_coin(coin_data)
        return coin
        
            
    async def create_tx(self, data: TransactionCreateRequestSchema, user_id: int) -> TransactionModel:
        
        coin = await self.get_or_create_coin(data.coin_id)
        coin_price = await self.get_price_by_cg_id(coin.cg_id)
        
        tx_data = TransactionCreateSchema(
            type=data.type,
            amount=data.amount,
            coin_id=data.coin_id,
            user_id=user_id,
            price=coin_price
        )
        tx = await self.repo.create_tx(tx_data)
        return tx
        
        
    async def get_all_user_tx(self, user_id: int):
        return await self.repo.get_all_txs_by_user_id(user_id)