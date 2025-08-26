from pydantic import BaseModel, Field
from typing import Optional, Literal, List

Action = Literal["buy", "sell"]
OrderType = Literal["market", "limit"]

class TradeIntent(BaseModel):
    action: Action
    ticker: str
    quantity: int = Field(gt=0)
    order_type: OrderType
    limit_price: Optional[float] = None

class TradeRequest(BaseModel):
    command: str

class ClarifyResponse(BaseModel):
    need_clarification: bool
    message: Optional[str] = None
    missing_fields: Optional[List[str]] = None
    parsed: Optional[TradeIntent] = None

class TradeResult(BaseModel):
    parsed: TradeIntent
    alpaca_response: dict
