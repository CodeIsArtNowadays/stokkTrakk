from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.portfolio.models import Coin, Transaction
from src.auth.models import User
from src.portfolio.schemas import (
    CoinCreateSchema,
    TransactionCreateSchema
)


class PortfolioRepository:
    
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create_coin(self, coin_data: CoinCreateSchema):
        coin = Coin(**coin_data.model_dump())
        self.session.add(coin)
        await self.session.flush()
        await self.session.refresh(coin)
        return coin
        
    async def get_coin_by_symbol(self, symbol: str):
        stmt = select(Coin).where(Coin.symbol == symbol)
        res = await self.session.execute(stmt)
        return res.scalar_one()
        
    async def get_coin_by_cg_id(self, cg_id: str):
        stmt = select(Coin).where(Coin.cg_id == cg_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
    
    async def create_tx(self, tx_data: TransactionCreateSchema):
        tx = Transaction(**tx_data.model_dump())
        self.session.add(tx)
        await self.session.flush()
        await self.session.refresh(tx)
        return tx
        
    async def get_all_txs_by_user_id(self, user_id: int):
        stmt = select(Transaction).where(Transaction.user_id==user_id)
        res = await self.session.execute(stmt)
        return res.scalars().all()
        
    async def get_all_user_coins(self, user_id: int) -> Sequence[str]:
        stmt = select(Coin.title).join(
            Transaction, Transaction.coin_id==Coin.cg_id
        ).join(
            User, Transaction.user_id==User.id
        ).where(
            Transaction.user_id==user_id
        ).group_by(Coin.title)
        
        res = await self.session.execute(stmt)
        return res.scalars().all()
        
    async def get_user_pnl(self, user_id: int):
        pass
        
    async def get_all_user_assets(self, user_id: int):
        pass
        
    