import json 

from aiohttp import ClientSession

from src.core.exceptions import ExternalAPIError
from src.portfolio.repository import PortfolioRepository
from config import settings
from src.portfolio.schemas import (
    CoinCreateSchema,
    TransactionCreateSchema,
    TransactionCreateWithCoinSchema,
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
                return data
    
    async def get_price_by_symbol(self, symbol):
        
        url = "https://api.coingecko.com/api/v3/coins/bitcoin" # testing
        session = ClientSession()
        
        async with session.get(url, params=self.params) as resp:
            data = json.loads(await resp.text())
            res = {
                'title': data['id'],
                'symbol': data['symbol'],
                'price': data['market_data']['current_price']['usd']
            }
            
            print(res)
        
    async def get_all_user_tx(self, user_id: int):
        return await self.repo.get_all_txs_by_user_id(user_id)
        
    
    async def create_tx(self, tx_data: TransactionCreateSchema):
        
        coin_is_available = True  # TODO
        if coin_is_available:  # TODO
            
            tx = await self.repo.create_tx(tx_data)
            return tx 
        raise  # TODO
            
    async def create_coin(self, coin_data: CoinCreateSchema):
        return await self.repo.create_coin(coin_data)
        
    async def create_tx_with_coin(self, data: TransactionCreateWithCoinSchema):
        coin_data = CoinCreateSchema(title=data.title, symbol=data.symbol)
        try: 
            async with self.repo.session.begin_nested():
                coin = await self.repo.create_coin(coin_data)
        except Exception:
            coin = await self.repo.get_coin_by_symbol(coin_data.symbol)
        tx_data = TransactionCreateSchema(
            type=data.type,
            amount=data.amount,
            price=data.price,
            user_id=data.user_id,
            coin_id=coin.id
        )
        tx = await self.repo.create_tx(tx_data)
        return tx