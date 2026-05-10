from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base
from src.core.literals import TxType
from src.auth.models import User



class Coin(Base):
    __tablename__ = 'coins'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    symbol: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None] = mapped_column(default=None)
    

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    type: Mapped[TxType] = mapped_column()
    amount: Mapped[Decimal] = mapped_column(Numeric())
    price: Mapped[Decimal] = mapped_column(Numeric())
    
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    coin_id: Mapped[int] = mapped_column(ForeignKey('coins.id'), index=True)
    
    coin: Mapped[Coin] = relationship(Coin, lazy='joined')
    user: Mapped[User] = relationship(User, lazy='joined') 
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )