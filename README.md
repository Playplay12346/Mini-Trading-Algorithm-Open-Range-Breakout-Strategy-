# Open-Range-Breakout-Strategy-Algorithm
This is a mini project that uses a Telegram Bot to send signals on Longs &amp; Shorts of a trade, using the Open Range Breakout Strategy with the help of ChatGPT<br>

<H2>Disclaimer</H2>
NOT FINANCIAL ADVICE: This is my own intrepretation of my algorithm, and by no means financial advice. I do not have even the basic certification or studied finance under any proper organisation, use the project at your own risk. This project is meant to be a small passion project and is created with the help of ChatGPT.

<H2>Summary of Project</H2>
This project is just a test to recall usages of APIs and test my financial knowledge, and is by no means any form of financial advice. The algorithm uses Open Range Breakout Strategy, with the timings of the stock martket to determine whether or not to go long or short on that particular product, whether it be ETFs or individual stocks etc. I tested it on a number of ETFs using different charts: 5m, 15m; on ETFS such as: SPY, QQQ, VOO or any form of leverage ETFs.

<H2>How to use this algorithm</H2>
Create your own telegram bot using tools such as Bot Father, input your own API and run it using a server, whether is cloud server or your own laptop for 24/7 or from Monday to Friday since the target of this algorithm is stocks or ETFs. Depending on the situation of the stock market and its volatility, we can edit the leverage rate and TP:SL, with more stable markets means ETFs movement will be slower hence a smaller TPSL, and a more volatile market means ETFs movement will be larger hence a larger TPSL. This is also directly linked to the product you are trading such as leveraged ETFs like the QQQ 3x Leverage ETF.

<H2>Testing parameters</H2>
I also included a script to test parameters of changes by pulling historical data of up to 60 days from Yahoo Finance. I tested the strategy, it was pretty decent averaging 20% returns on 60 days. For me personally, the best result I had was using 15m chart on QQQ, as using a smaller timeframe chart although having more data, it will include more noise that results in more misread of the market conditions.

<H2>Future Improvements</H2>
Few other improvements I can think of: <br>
1. Using VIX &/or order books as indicators to calculate the volatility of the market of that day, while comparing it to the previous days (maybe 2-3 days worth) volatility to determine the TPSL for the day, creating a dynamic TPSL approach, as I realised that sometimes the TPSL is too small, causing inconsistencies when we try to play out the trade, such as we buy LONG, due to volatility the price drop to a certain level and hit out SL for the day, but jumps back up later to hit way more than our TP, this is due to not taking into account volatity of the day which results in a failed trade. <br>
2. Create a sort of model to take into account news, such as reports release, speeches by the Fed memebers or President, or any news that would potentially affect the trade, however I have not thought of how to combine it with openrange breakout strategy yet, and for now if implemented can only stop the trade of the day.
3. Automatically close trade 10 minutes before market closes, this is to combat the situation where we expected too much volatility and instead price swings half way, we can maybe slightly lower the TP or immediate close the trade on a loss to avoid holding the position overnight to prevent any potentially risk of being liquidated or bag holding.

