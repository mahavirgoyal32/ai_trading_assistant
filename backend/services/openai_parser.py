from typing import Tuple, Dict, Any, List
import re
from . import schemas_guard
from models import TradeIntent
from utils import MOCK_OPENAI, OPENAI_API_KEY

# Optional: strict JSON schema for function calling
trade_schema = {
    "name": "extract_trade_intent",
    "description": "Extract trading intent from natural language.",
    "parameters": {
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["buy", "sell"]},
            "ticker": {"type": "string"},
            "quantity": {"type": "integer", "minimum": 1},
            "order_type": {"type": "string", "enum": ["market", "limit"]},
            "limit_price": {"type": "number"}
        },
        "required": ["action", "ticker", "quantity", "order_type"]
    }
}

# --- MOCK PARSER (regex + heuristics) ---
TICKER_WORDS = {
    "apple": "AAPL", "appl": "AAPL", "aapl": "AAPL",
    "tesla": "TSLA", "tsla": "TSLA",
    "nvidia": "NVDA", "nvda": "NVDA",
    "microsoft": "MSFT", "msft": "MSFT",
}

_qty = re.compile(r"(\d{1,9})\s*(shares?|sh)?", re.I)
_price = re.compile(r"\$\s*([0-9]+(?:\.[0-9]+)?)", re.I)

# very small helper to guess ticker token (alnum <=5)
_ticker_token = re.compile(r"\b([A-Z]{1,5})\b")


def parse_with_mock(text: str) -> Dict[str, Any]:
    t = text.lower()
    action = "buy" if "sell" not in t and ("buy" in t or "long" in t) else ("sell" if "sell" in t or "short" in t else None)

    quantity = None
    m = _qty.search(t)
    if m:
        quantity = int(m.group(1))

    # ticker by name map first
    ticker = None
    for word, sym in TICKER_WORDS.items():
        if word in t:
            ticker = sym
            break
    if not ticker:
        caps = _ticker_token.findall(text.upper())
        # choose first plausible token not in stopwords
        stop = {"BUY","SELL","SHARES","AT","MARKET","LIMIT","FOR"}
        for tok in caps:
            if tok not in stop and 1 <= len(tok) <= 5:
                ticker = tok
                break

    price = None
    m2 = _price.search(text)
    if m2:
        price = float(m2.group(1))

    order_type = "limit" if price is not None or "limit" in t else "market" if "market" in t or price is None else None

    data = {"action": action, "ticker": ticker, "quantity": quantity, "order_type": order_type}
    if order_type == "limit" and price is not None:
        data["limit_price"] = price
    return data


def parse_trade_command(text: str) -> Tuple[dict, List[str]]:
    """Return (parsed_dict, missing_fields[]) using either OpenAI or mock parser."""
    if MOCK_OPENAI:
        parsed = parse_with_mock(text)
    else:
        # Real OpenAI function calling
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": text}],
            tools=[{"type": "function", "function": trade_schema}],
            tool_choice="auto",
        )
        call = resp.choices[0].message.tool_calls[0]
        parsed = schemas_guard.safe_json(call.function.arguments)

    required = ["action", "ticker", "quantity", "order_type"]
    missing = [k for k in required if not parsed.get(k)]
    if parsed.get("order_type") == "limit" and not parsed.get("limit_price"):
        missing.append("limit_price")
    return parsed, missing
