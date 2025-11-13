import ollama
import yfinance as yf
from typing import Callable, Dict, Any

def get_stock_price(symbol: str) -> float:
    ticket = yf.Ticker(symbol)
    return ticket.info.get('regularMarketPrice') or ticket.fast_info.last_price

def get_company_info(symbol: str) -> Dict[str, Any]:
    ticket = yf.Ticker(symbol)
    info = ticket.info
    company_info = {
        'name': info.get('longName'),
        'sector': info.get('sector'),
        'industry': info.get('industry'),
        'market_cap': info.get('marketCap'),
        'website': info.get('website'),
    }
    return company_info

def get_price_history(symbol: str, period: str = "1mo", interval: str = "1d") -> Dict[str, Any]:
    ticket = yf.Ticker(symbol)
    history = ticket.history(period=period, interval=interval)
    return history.to_dict()

# Simulación de un prompt
prompt = "What is the stock price of Apple? Or tell me about Apple Inc. Or give me Apple's price history for the last week."

available_actions: Dict[str, Callable] = {
    'get_stock_price': get_stock_price,
    'get_company_info': get_company_info,
    'get_price_history': get_price_history,
}

response = ollama.chat(
    'mistral',
    messages=[{'role': 'user', 'content': prompt}],
    tools=[get_stock_price, get_company_info, get_price_history],
)

if response.message.tool_calls:
    for tool in response.message.tool_calls:
        function_to_call = available_actions.get(tool.function.name)
        if function_to_call:
            print('Calling function:', tool.function.name)
            print('With arguments:', tool.function.arguments)
            print('Function output:', function_to_call(**tool.function.arguments))
        else:
            print('Function not available:', tool.function.name)
