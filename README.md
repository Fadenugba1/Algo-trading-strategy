# Algo-trading-strategy

This is an algorithmic trading project, written in python, which uses utilises technical analysis to perform to generate trades.

This project was initially built in August 2025 during my work experience at G-Research, performing technical analysis utilising a simple moving average strategy with ATR volatility filtering. I have since further developed the project to implement more technical indicators such as rsi, bollinger bands and rejection candles.

This code can :
    perform a backtest on the bollinger band, rejection candle, moving average crossover strategy(seen in strat.ipynb)
    has implemented technical indicators such as RSI,bollinger bands,rejection candles,stochastic oscillator, ADX, OBV(seen in indicators.py)


## Results:
    From 100% starting equity returns generated 170% revenue
    There is a period within the last 800 days where the stratgey generates 144% revenue
    Generates very small sharpe ratio of approximately 0.058

## Conclusions:
    Has very large drawdowns potentially due to over-allocating on a particular trade. This could be due to the large max allocation of 0.4
    Very small Sharpe Ratio as the volatility of returns is quite high
    Underperforms buy and hold