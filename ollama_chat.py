import ollama
import yfinance as yf
from typing import Callable, Dict, Any

def get_stock_price(simbol  : str) -> float:
    ticket = yf.Ticker(simbol)
    return ticket.info.get('regularMarketPrice') or ticket.fast_info.last_price

prompt = "What's the stock price of Apple?"

available_actions: Dict[str, Callable] = {
    'get_stock_price': get_stock_price,
}

response = ollama.chat(
    'mistral',
    messages=[{'role':'user', 'content':prompt}],
    tools=[get_stock_price],
)

if response.message.tool_calls:
    for tool in response.message.tool_calls:
        if function_to_call := available_actions.get(tool.function.name):
            print('calling function:', tool.function.name)
            print('with arguments:', tool.function.arguments)
            print('function output:', function_to_call(**tool.function.arguments))
        else:
            print('function not available:', tool.function.name)