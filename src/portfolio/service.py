import json 

from aiohttp import ClientSession

from src.portfolio.repository import PortfolioRepository
from config import settings
from src.portfolio.schemas import CoinCreateSchema, TransactionCreateSchema

class PortfolioService:
    def __init__(self, repo: PortfolioRepository): # testing
        self.repo = repo
        self.api_token = settings.COINGECKO_API_KEY
        
        
    async def get_price_by_symbol(self, symbol):
        
        params = {"x-cg-demo-api-key": self.api_token}
        url = "https://api.coingecko.com/api/v3/coins/bitcoin" # testing
        session = ClientSession()
        
        async with session.get(url, params=params) as resp:
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