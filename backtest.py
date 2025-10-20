# Dynamic leveraging
import yfinance as yf
import pandas as pd
import numpy as np

# --- PARAMETERS ---
symbol = "QQQ"
interval = "15m"
period = "60d"  # last 60 days
tp_percent = 0.0015   # Take Profit 0.15%
sl_percent = 0.001    # Stop Loss 0.1%
capital = 1000
risk_per_trade = 0.2  # 20% of capital per trade
leverage = 5     

# --- FETCH DATA ---
def get_data(symbol, interval, period):
    df = yf.download(tickers=symbol, interval=interval, period=period)
    df = df[['Open', 'High', 'Low', 'Close']].copy()
    df.dropna(inplace=True)
    df.index = pd.to_datetime(df.index)
    df['Date'] = df.index.date
    return df

# --- IDENTIFY ORB ---
def get_orb_candles(df):
    orb_candles = df.groupby('Date').first()[['High', 'Low']]
    return orb_candles

# --- GENERATE TRADES (adjustable leverage) ---
def generate_trades(df, orb_candles):
    trades = []
    for day, orb in orb_candles.iterrows():
        day_data = df[df['Date'] == day]
        orb_high = orb['High'].item()
        orb_low = orb['Low'].item()

        for idx, row in day_data.iterrows():
            close = row['Close'].item()
            max_risk_dollars = capital * risk_per_trade

            if close > orb_high:  # LONG
                entry = close
                sl_price = entry * (1 - sl_percent)
                position_size = max_risk_dollars / (entry - sl_price)

                # --- enforce leverage ---
                max_affordable_size = (capital * leverage) / entry
                position_size = min(position_size, max_affordable_size)

                trades.append({
                    'Date': idx,
                    'Type': 'LONG',
                    'Entry': entry,
                    'TP': entry * (1 + tp_percent),
                    'SL': sl_price,
                    'Size': position_size
                })
                break

            elif close < orb_low:  # SHORT
                entry = close
                sl_price = entry * (1 + sl_percent)
                position_size = max_risk_dollars / (sl_price - entry)

                # --- enforce leverage ---
                max_affordable_size = (capital * leverage) / entry
                position_size = min(position_size, max_affordable_size)

                trades.append({
                    'Date': idx,
                    'Type': 'SHORT',
                    'Entry': entry,
                    'TP': entry * (1 - tp_percent),
                    'SL': sl_price,
                    'Size': position_size
                })
                break

    return trades

# --- CALCULATE PnL ---
def calculate_pnl(trades, df):
    total_pnl = 0.0
    for trade in trades:
        day_data = df[df.index.date == trade['Date'].date()]
        highs = day_data['High'].to_numpy()
        lows = day_data['Low'].to_numpy()
        close_prices = day_data['Close'].to_numpy()

        entry = trade['Entry']
        tp = trade['TP']
        sl = trade['SL']
        size = trade['Size']

        pnl = 0.0
        if trade['Type'] == 'LONG':
            hit_tp = np.any(highs >= tp)
            hit_sl = np.any(lows <= sl)
            if hit_tp:
                pnl = (tp - entry) * size
            elif hit_sl:
                pnl = (sl - entry) * size
            else:
                pnl = (close_prices[-1] - entry) * size
        else:  # SHORT
            hit_tp = np.any(lows <= tp)
            hit_sl = np.any(highs >= sl)
            if hit_tp:
                pnl = (entry - tp) * size
            elif hit_sl:
                pnl = (entry - sl) * size
            else:
                pnl = (entry - close_prices[-1]) * size

        total_pnl += pnl

    return float(total_pnl)

# --- MAIN ---
data = get_data(symbol, interval, period)
orb_candles = get_orb_candles(data)
trades = generate_trades(data, orb_candles)
pnl = calculate_pnl(trades, data)

print(f"Leverage used: {leverage}:1")
print(f"Total trades: {len(trades)}")
print(f"Total PnL: ${pnl:.2f}")
for t in trades:
    print(t)
