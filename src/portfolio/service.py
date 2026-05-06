import json 

from aiohttp import ClientSession

from src.portfolio.repository import PortfolioRepository
from config import settings

class PortfolioService:
    def __init__(self, repo: PortfolioRepository | None = None): # testing
        self.repo = repo
        self.api_token = settings.COINGECKO_API_KEY
        self.session = ClientSession()
        
        
    async def get_price_by_symbol(self, symbol):
        
        params = {"x-cg-demo-api-key": self.api_token}
        url = "https://api.coingecko.com/api/v3/coins/bitcoin" # testing
        
        async with self.session.get(url, params=params) as resp:
            data = json.loads(await resp.text())
            res = {
                'title': data['id'],
                'symbol': data['symbol'],
                'price': data['market_data']['current_price']['usd']
            }
            
            print(res)
        
portfolio_service = PortfolioService() # testing
