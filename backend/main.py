from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import TradeRequest, ClarifyResponse, TradeIntent, TradeResult
from services.openai_parser import parse_trade_command
from services.alpaca import place_order
from utils import ALLOWED_ORIGINS

app = FastAPI(title="AI Trading Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/trade", response_model=TradeResult | ClarifyResponse)
def trade(req: TradeRequest):
    parsed, missing = parse_trade_command(req.command)
    if missing:
        msg = _clarify_message(req.command, missing)
        return ClarifyResponse(need_clarification=True, message=msg, missing_fields=missing)

    intent = TradeIntent(**parsed)
    alpaca_resp = place_order(
        action=intent.action,
        ticker=intent.ticker,
        quantity=intent.quantity,
        order_type=intent.order_type,
        limit_price=intent.limit_price,
    )
    return TradeResult(parsed=intent, alpaca_response=alpaca_resp)


def _clarify_message(cmd: str, missing: list[str]) -> str:
    prompts = []
    if "ticker" in missing:
        prompts.append("Which stock ticker?")
    if "quantity" in missing:
        prompts.append("How many shares?")
    if "limit_price" in missing:
        prompts.append("What limit price?")
    return " I need a bit more info: " + " ".join(prompts)
