from pydantic import BaseModel, ConfigDict, computed_field, field_validator

from src.auth.schemas import UserInfoSchema
from src.core.types import TxType, CryptoSymbol, PositiveDecimal


class BaseSchema(BaseModel):
    
    model_config = ConfigDict(
        from_attributes=True
    )


class CoinCreateSchema(BaseModel):
    title: str
    symbol: CryptoSymbol
    cg_id: str
    

class CoinMiniRetrieveSchema(BaseSchema):
    symbol: CryptoSymbol
    cg_id: str
    

class CoinInfoSchema(BaseSchema):
    title: str
    symbol: CryptoSymbol
    cg_id: str
    
    
class TransactionBaseSchema(BaseSchema):
    type: TxType
    amount: PositiveDecimal


class TransactionCreateRequestSchema(TransactionBaseSchema):
    coin_id: str
    
    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: PositiveDecimal) -> PositiveDecimal:
        if v > 1_000_000:
            raise ValueError('Amount more than a 1M')
        return v


class TransactionCreateSchema(TransactionCreateRequestSchema):
    user_id: int
    price: PositiveDecimal
    
    @field_validator('price')
    @classmethod
    def validate_price(cls, v: PositiveDecimal) -> PositiveDecimal:
        if v > 10_000_000:
            raise ValueError('Price more than 10M')
        return v


class TransactionRetrieveSchema(TransactionBaseSchema):
    id: int
    user: UserInfoSchema
    coin: CoinMiniRetrieveSchema
    price: PositiveDecimal
    
    @computed_field
    @property
    def total_worth(self) -> PositiveDecimal:
        return self.amount * self.price

