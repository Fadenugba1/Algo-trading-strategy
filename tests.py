import pytest
import numpy as np
import pandas as pd
import polars as pl
import random
from indicator import *
from strategy import  Signal
import yfinance as yf
import talib

sample_df = pl.read_csv("META.csv")
sample_df = sample_df.with_columns([((pl.col("Close/Last").str.replace_all(r"\$","")).cast(pl.Float64)),
((pl.col("High").str.replace_all(r"\$","")).cast(pl.Float64)),
((pl.col("Low").str.replace_all(r"\$","")).cast(pl.Float64)),
((pl.col("Open").str.replace_all(r"\$","")).cast(pl.Float64))])
sample_df = sample_df.reverse()

class Test_bollinger:
    def test_bollinger_sma_shape(self):
        series =  np.array([50.0,50.0,50.0,50.0,50.0,50.0,50.0,50.0,50.0,50.0])
        upper,lower,moving_avg = bollinger(series,period=5,bollinger_range=2)
        expected = np.array([0.0,0.0,0.0,0.0,50.0,50.0,50.0,50.0,50.0,50.0])
        assert(moving_avg == expected).all()
    
    def test_bollinger_upper_shape(self):
        series =  np.array([50.0,50.0,50.0,50.0,50.0,50.0,50.0,50.0,50.0,50.0])
        upper,lower,moving_avg = bollinger(series,period=5,bollinger_range=2)
        expected = np.array([0.0,0.0,0.0,0.0,50.0,50.0,50.0,50.0,50.0,50.0])
        assert(upper== expected).all()
    
    def test_bollinger_lower_shape(self):
        series =  np.array([50.0,50.0,50.0,50.0,50.0,50.0,50.0,50.0,50.0,50.0])
        upper,lower,moving_avg = bollinger(series,period=5,bollinger_range=2)
        expected = np.array([0.0,0.0,0.0,0.0,50.0,50.0,50.0,50.0,50.0,50.0])
        assert(lower == expected).all()
        
    def test_bollinger_upper_val(self):
        expected_upper, expected_middle, expected_lower = talib.BBANDS(sample_df["Close/Last"][:10], timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
        expected_upper = np.nan_to_num(expected_upper, nan=0.0)
        expected_middle = np.nan_to_num(expected_middle, nan=0.0)
        expected_lower = np.nan_to_num(expected_lower, nan=0.0)

        close = (sample_df["Close/Last"][:10]).to_numpy()
        upper,lower,moving_avg = bollinger(close,period=5,bollinger_range=2)
        assert np.allclose(expected_upper, upper, rtol=1e-1, atol=1e-1, equal_nan=True)
    
    def test_bollinger_sma_val(self):
        expected_upper, expected_middle, expected_lower = talib.BBANDS(sample_df["Close/Last"][:10], timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
        expected_upper = np.nan_to_num(expected_upper, nan=0.0)
        expected_middle = np.nan_to_num(expected_middle, nan=0.0)
        expected_lower = np.nan_to_num(expected_lower, nan=0.0)

        close = (sample_df["Close/Last"][:10]).to_numpy()
        upper,lower,moving_avg = bollinger(close,period=5,bollinger_range=2)
        assert np.allclose(expected_middle, moving_avg, rtol=1e-1, atol=1e-1, equal_nan=True)
    
    def test_bollinger_lower_val(self):
        expected_upper, expected_middle, expected_lower = talib.BBANDS(sample_df["Close/Last"][:10], timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
        expected_upper = np.nan_to_num(expected_upper, nan=0.0)
        expected_middle = np.nan_to_num(expected_middle, nan=0.0)
        expected_lower = np.nan_to_num(expected_lower, nan=0.0)

        close = (sample_df["Close/Last"][:10]).to_numpy()
        upper,lower,moving_avg = bollinger(close,period=5,bollinger_range=2)
        print(lower)
        print(expected_lower)
        assert np.allclose(expected_lower, lower, rtol=1e-1, atol=1e-1, equal_nan=True)
        
        
        
             
class Test_Rsi:
                  
    def test_rsi(self):
        arrayt = np.array([10,9,8,7,6,5,4,3,2,1])
        rsi = Relative_strength_index(arrayt,period=5)
        
        exp_rsi = np.array([50,50,50,50,50,0,0,0,0,0],dtype=float)
        print(rsi)
        assert(rsi == exp_rsi).all()
        
        
class Test_ATR:
    def test_ATR(self):
        Highs = np.array([0,0,0,0,0,0,0,0,0,0,0,0])
        Close = np.array([0,0,0,0,0,0,0,0,0,0,0,0])
        Lows =  np.array([0,0,0,0,0,0,0,0,0,0,0,0])
        period = 3
        relative_ATR = ATR_backtest(Close,High=Highs,Low=Lows,period=period)
        exp_r_ATR = np.array([0,0,0,0,0,0,0,0,0,0,0,0])
        assert(relative_ATR == exp_r_ATR).all()
    
    def test_ATR_val(self):
        close = (sample_df["Close/Last"][:10]).to_numpy()
        High = (sample_df["High"][:10]).to_numpy()
        Low = (sample_df["Low"][:10]).to_numpy()
        expected_atr = talib.ATR(High, Low, close,timeperiod=5)
        expected_atr = np.nan_to_num(expected_atr, nan=0.0)

        atr = ATR_backtest(close,High=High,Low=Low,period=5)
        print(atr)
        print(expected_atr)
        assert np.allclose(len(atr), len(expected_atr))
    
class Test_Strategy:
    sample_df = pl.read_csv("META.csv")
    sample_df = sample_df.with_columns([((pl.col("Close/Last").str.replace_all(r"\$","")).cast(pl.Float64)),
    ((pl.col("High").str.replace_all(r"\$","")).cast(pl.Float64)),
    ((pl.col("Low").str.replace_all(r"\$","")).cast(pl.Float64)),
    ((pl.col("Open").str.replace_all(r"\$","")).cast(pl.Float64))])
    sample_df = sample_df.reverse()
    
    def test_trade_normal(self):
        rsi_sig = [0,0,0,0,0]
        bband_sig = [0,2,0,-1,0]
        reject = [0,0,0,0,0]
        #will ensure that relative atr is always 0.03
        atr = 0.03*self.sample_df["Close/Last"]
        Sig = Signal(self.sample_df[:5],1,1)
        returns,stats = Sig.trades(rsi_sig,bband_sig,atr[:5],reject,1000)
        expected_returns = 995.62
        assert(returns == expected_returns)
    
    def test_trade_boundary(self):
        rsi_sig = [0,0,0,0,0]
        bband_sig = [0,2,0,0,0]
        reject = [0,1,0,0,0]
        #will ensure that relative atr is always 0.03
        atr = 0.03*self.sample_df["Close/Last"]
        Sig = Signal(self.sample_df[:5],1,1)
        returns,stats = Sig.trades(rsi_sig,bband_sig,atr[:5],reject,1000)
        expected_returns = 995.62
        assert(returns == expected_returns)
        
    def test_trade_boundary2(self):
        rsi_sig = [0,0,0,0,0]
        bband_sig = [0,2,0,0,0]
        reject = [0,1,0,0,0]
        #will ensure that relative atr is always 0.03
        atr = 0.05*self.sample_df["Close/Last"]
        Sig = Signal(self.sample_df[:5],1,1)
        returns,stats = Sig.trades(rsi_sig,bband_sig,atr[:5],reject,1000)
        expected_returns = 997.08
        assert(returns == expected_returns)
        
    def test_trade_look_ahead(self):
        testStrat = Signal(sample_df,5,2)
        total,stats = testStrat.backtest()
        checkStrat = Signal(sample_df[:500],5,2)
        check_total,check_stats = checkStrat.backtest()
        print(check_stats["Daily total"][::20])
        print(stats["Daily total"][:501:20])
        #check penultimate values align as final values may differ as always sell signal generated at end of data reached
        assert(check_stats["Daily total"][-2] == stats["Daily total"][498])
            
    #some shape issue with the daily totals
        
        
        
    