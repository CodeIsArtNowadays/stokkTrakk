from decimal import Decimal
from typing import Annotated, Literal

from pydantic import Field, StringConstraints


TxType = Literal['buy', 'sell']
PositiveDecimal = Annotated[Decimal, Field(ge=0, decimal_places=8)]
CryptoSymbol = Annotated[str, StringConstraints(min_length=2, max_length=10, to_upper=True)]