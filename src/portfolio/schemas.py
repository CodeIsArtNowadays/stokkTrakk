from decimal import Decimal

from pydantic import BaseModel

from src.auth.schemas import UserInfoSchema
from src.core.literals import TxType


class CoinCreateSchema(BaseModel):
    title: str
    symbol: str
    

class CoinMiniRetrieveSchema(BaseModel):
    id: int
    symbol: str
    

class CoinInfoSchema(BaseModel):
    id: int
    title: str
    symbol: str
    
    
class TransactionBaseSchema(BaseModel):
    type: TxType
    amount: Decimal
    price: Decimal


class TransactionCreateRequestSchema(TransactionBaseSchema):
    coin_id: int


class TransactionCreateSchema(TransactionCreateRequestSchema):
    user_id: int


class TransactionCreateWithCoinRequestSchema(TransactionBaseSchema, CoinCreateSchema):
    pass
    
class TransactionCreateWithCoinSchema(TransactionCreateWithCoinRequestSchema):
    user_id: int


class TransactionRetrieveSchema(TransactionBaseSchema):
    id: int
    user: UserInfoSchema
    coin: CoinMiniRetrieveSchema
    
