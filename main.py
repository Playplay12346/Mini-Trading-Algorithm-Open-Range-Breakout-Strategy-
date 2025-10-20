# === ORB Breakout Strategy with Telegram Alerts ===

import yfinance as yf
import pandas as pd
import numpy as np
import time
import requests
import datetime

# === TELEGRAM SETUP ===
BOT_TOKEN = ""     # replace with your BotFather token
CHAT_ID = ""         # replace with your chat_id

def send_signal(message):
    """Send a message to Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Telegram error:", e)

# === STRATEGY PARAMETERS ===
symbol = ""
interval = ""
tp_percent =    # Take Profit 
sl_percent =     # Stop Loss 
capital = 
risk_per_trade = 
leverage = 

# === FETCH DATA ===
def get_data(symbol, interval, period="2d"):
    df = yf.download(tickers=symbol, interval=interval, period=period)
    df = df[['Open', 'High', 'Low', 'Close']].copy()
    df.dropna(inplace=True)
    df.index = pd.to_datetime(df.index)
    df['Date'] = df.index.date
    return df

# === ORB LEVELS (first 5m candle of each day) ===
def get_orb_levels(df):
    orb_candles = df.groupby('Date').first()[['High', 'Low']]
    return orb_candles

# === Check if a signal is triggered ===
def check_signal(df, orb_candles):
    today = df.index[-1].date()
    orb = orb_candles.loc[today]

    # Convert Series to floats safely
    orb_high = float(orb['High'].iloc[0])
    orb_low  = float(orb['Low'].iloc[0])
    last_close = float(df['Close'].iloc[-1])
    max_risk_dollars = capital * risk_per_trade

    if last_close > orb_high:  # LONG
        entry = last_close
        sl_price = entry * (1 - sl_percent)
        position_size = max_risk_dollars / (entry - sl_price)
        max_affordable_size = (capital * leverage) / entry
        position_size = min(position_size, max_affordable_size)

        return f"🚀 LONG {symbol} @ {entry:.2f}\nTP: {entry*(1+tp_percent):.2f}\nSL: {sl_price:.2f}\nSize: {position_size:.2f}"

    elif last_close < orb_low:  # SHORT
        entry = last_close
        sl_price = entry * (1 + sl_percent)
        position_size = max_risk_dollars / (sl_price - entry)
        max_affordable_size = (capital * leverage) / entry
        position_size = min(position_size, max_affordable_size)

        return f"🔻 SHORT {symbol} @ {entry:.2f}\nTP: {entry*(1-tp_percent):.2f}\nSL: {sl_price:.2f}\nSize: {position_size:.2f}"

    return None


print("📡 ORB Bot started... sending signals to Telegram")

last_checked = None
last_heartbeat = None
heartbeat_interval = 60 * 30  # 30 minutes
started = False

while True:
    try:
        if started is False:
            send_signal("⭐Bot has started!")
            started = True
         # 1️⃣ Fetch last 2 days of 5-min data
        data = get_data(symbol, interval, period="2d")

        # 2️⃣ Skip iteration if no data (market closed)
        if data.empty:
            print("⚠️ No data available — market may be closed.")
            now = datetime.datetime.now()
            # Still send heartbeat if interval reached
            if last_heartbeat is None or (now - last_heartbeat).total_seconds() >= heartbeat_interval:
                send_signal(f"💓 Bot is running (market closed). Time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
                last_heartbeat = now
            time.sleep(60)
            continue

        orb_candles = get_orb_levels(data)

        # 3️⃣ Get timestamp of last completed 5-min bar
        last_bar_time = data.index[-1]
        today = pd.Timestamp.now().date()
        now = datetime.datetime.now()

        # 4️⃣ Only check signal if last bar is today
        if last_bar_time.date() == today:
            if last_checked is None or last_bar_time > last_checked:
                signal = check_signal(data, orb_candles)
                if signal:
                    send_signal(signal)
                    print("Signal sent:", signal)

                last_checked = last_bar_time

        # 5️⃣ Send heartbeat every 30 minutes, independent of signals
        if last_heartbeat is None or (now - last_heartbeat).total_seconds() >= heartbeat_interval:
            send_signal(f"💓 Bot is running. Time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Heartbeat sent at {now}")
            last_heartbeat = now

    except Exception as e:
        send_signal(f"⚠️ Bot error: {e}")
        print("Error:", e)

    # 6️⃣ Wait before checking again
    time.sleep(60)  # check every 1 minute
