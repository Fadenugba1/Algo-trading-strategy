import numpy as np
import pandas as pd
import polars as pl
import plotly as plt

#calculates the relative strength index from the input series
def Relative_strength_index(series,**kwargs):
  close_arr = pd.Series(series,dtype=np.float64)
  delta = close_arr.diff()
  delta = delta.dropna()
  period = kwargs["period"]
  gains = delta.clip(lower=0.0)
  losses = -delta.clip(upper=0.0)
  avg_gains = gains.rolling(period).mean()
  avg_losses = losses.rolling(period).mean()
  relative_strength = avg_gains/avg_losses
  RS_index = 100 - (100/(1+relative_strength))
  RS_index = RS_index.fillna(50)
  RS_index = np.insert(RS_index.to_numpy(dtype=np.float64),0,50.0)
  return RS_index


#calculates the bollinger bands from the input series
def bollinger(series,**kwargs):
  period = kwargs["period"]
  bollinger_range = kwargs["bollinger_range"]
  series = pd.Series(series)
  moving_avg = series.rolling(period).mean().fillna(0)
  std = series.rolling(period).std()
  upper_band = (moving_avg + (bollinger_range*std)).fillna(0)
  lower_band = moving_avg - (bollinger_range*std).fillna(0)
  return upper_band.to_numpy(),lower_band.to_numpy(),moving_avg.to_numpy()

#calculates the average true range from the input series
def ATR_backtest(close,**kwargs):
  Highs = np.array(kwargs["High"])
  Lows = np.array(kwargs["Low"])
  Close = np.array(close)
  period = kwargs["period"]
  TR = [0.0]
  for i in range(1,len(Highs)):
    HL = Highs[i]-Lows[i]
    HCPrev = Highs[i]-Close[i-1]
    HCPrev= np.abs(HCPrev)
    LCPrev = Lows[i] - Close[i-1]
    LCPrev = np.abs(LCPrev)
    current_TR = max(HL, HCPrev,LCPrev)
    TR.append(current_TR)
  ATR = pd.Series(TR).rolling(period).mean().fillna(0)
  #ATR = np.insert(ATR.to_numpy(),0,0.0)
  return ATR

#identifies rejection candles from the input series
def rejection_candles(close,**kwargs):
  signals = []
  Close = close
  Highs = np.array(kwargs["High"])
  Lows = np.array(kwargs["Low"])
  Open = np.array(kwargs["Open"])
  for i in range(0,len(Close)):
    if ((min(Open[i],Close[i])-Lows[i])>(1.5*abs(Close[i]-Open[i])) and
        (Highs[i]-max(Close[i],Open[i]))< (0.8*abs(Open[i]-Close[i])) and
        (abs(Open[i]-Close[i])>Open[i]*0.001)):
      signals.append(1)
    elif ((Highs[i]-max(Close[i],Open[i]))>(1.5*abs(Close[i]-Open[i])) and
        (min(Open[i],Close[i])-Lows[i])< (0.8*abs(Open[i]-Close[i])) and
        (abs(Open[i]-Close[i])>Open[i]*0.001)):
      signals.append(-1)
    else:
      signals.append(0)
  return signals
      
  


