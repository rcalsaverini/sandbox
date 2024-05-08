from enum import Enum
from typing import List, Tuple
import yfinance as yf
import pandas as pd
import datetime as dt

class Action(Enum):
        BUY = 1
        SELL = 2
        HOLD = 3

History = pd.DataFrame

def get_optimal_action(current_price: float, history: History, margin: float) -> Action:
    profit_at_best_long = (history["price"].max() - current_price) / current_price
    profit_at_best_short = (current_price - history["price"].min()) / current_price
    if max(profit_at_best_long, profit_at_best_short) > margin:
        return Action.BUY if profit_at_best_long > profit_at_best_short else Action.SELL
    else:
        return Action.HOLD
    
def make_examples(history: History, margin: float, window: int) -> List[Tuple[History, Action]]:
    output = []
    for row in history.itertuples():
        past_history = history\
            .loc[history.timestamp < row.timestamp]
            
        future_history = history\
            .loc[history.timestamp > row.timestamp]\
            .iloc[:window]
        if (len(future_history) < window) or (len(past_history) < window):
            continue

        current_price = row.price
        optimal_action = get_optimal_action(current_price, future_history, margin)
        output.append((row.timestamp, row.price, past_history.price.values, future_history.price.values, optimal_action.name))
    return pd.DataFrame(output, columns=["timestamp", "current_price", "past_history", "future_history", "optimal_action"])



if __name__ == "__main__":
    tickers = [
        'GOOG', 'MSFT', 'NU', '^BVSP', 'NVDA', 'PETR4.SA', 'VALE3.SA', 
        'BBAS3.SA', 'ITUB4.SA', 'ITSA4.SA', 'MGLU3.SA', 'WEGE3.SA',
        'ABEV3.SA', 'CIEL3.SA', 'BRFS3.SA', 'JBSS3.SA', 'GGBR4.SA',
        'BBDC4.SA', 'USIM5.SA'
    ]
    start = dt.datetime.today() - dt.timedelta(days=365 * 20)
    end = dt.datetime.today()
    total_examples = 0
    for ticker in tickers:
        df = yf.Ticker(ticker).history(period='1d', start=start, end=end).reset_index(inplace=False).loc[:, ["Date", "Close"]]
        df.columns = ["timestamp", "price"]
        examples = make_examples(df, 0.02, 30)
        print(f"{ticker}: has {len(examples)} examples")
        total_examples += len(examples)
        examples.to_parquet(f"{ticker.replace("^", "_")}.parquet")

    print(f"Total examples: {total_examples}")
        

