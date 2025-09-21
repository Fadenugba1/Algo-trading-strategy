from indicator import *
class Signal:
    def __init__(self,data,period,bollinger_range):
        self.dataframe = data
        self.period = period
        self.bollinger_range = bollinger_range
        self.fee_rate = 0.001
        self.sma = pd.Series(self.dataframe["Close/Last"]).rolling(50).mean()
        self.sma = self.sma.fillna(0)
        self.fma = pd.Series(self.dataframe["Close/Last"]).rolling(5).mean()
        self.fma = self.fma.fillna(0)
        
        
    def relative_strength_index(self):
        rsi = Relative_strength_index(self.dataframe["Close/Last"],period=self.period)
        return rsi
    
    def bollinger_bands(self):
        upper,lower,ma = bollinger(self.dataframe["Close/Last"],period=self.period,bollinger_range=self.bollinger_range)
        return upper,lower,ma
    
    def Average_True(self):
        return ATR_backtest(self.dataframe["Close/Last"],High=self.dataframe["High"],Low =self.dataframe["Low"],period = self.period)
    
    def relative_strength_index_signal(self,rsi):
        rsi_signal = [0]
        for i in range(1,len(rsi)):
            if rsi[i]>rsi[i-1]:
                if rsi[i]<30:
                    rsi_signal.append(2)
                elif rsi[i]>70:
                    rsi_signal.append(-1)
                else:
                    rsi_signal.append(0)
            elif rsi[i]>30 and rsi[i-1]<30:
                rsi_signal.append(1)
            elif rsi[i]>70 and rsi[i-1]<70:
                rsi_signal.append(-1)
            else:
                rsi_signal.append(0)
        return rsi_signal
    
    
    def bollinger_band_signal(self,upper_band,lower_band,moving_avg):
        bband_signal = [0]
        for i in range(1,len(upper_band)):
            if self.dataframe["Close/Last"][i] < moving_avg[i]:
                if self.dataframe["Close/Last"][i] > lower_band[i] and self.dataframe["Close/Last"][i-1] < lower_band[i-1]:
                    bband_signal.append(2)
                else:
                    bband_signal.append(1)
            elif self.dataframe["Close/Last"][i] < upper_band[i] and self.dataframe["Close/Last"][i-1] > upper_band[i-1]:
                bband_signal.append(-1)
            else:
                bband_signal.append(0)
        return bband_signal
    
    def rejection_candles_signal(self,Close,High,Open,Low):
        signal = rejection_candles(Close,High=High,Low=Low,Open=Open)
        return signal
        
    def buy(self,total,lot_size,current_price,buy_arr,signal):
        trade = lot_size * current_price
        fee = self.fee_rate*trade
        if trade + fee < total:
            total = total -trade-fee
            state = "buy"
            buy_arr.append(trade)
            signal.append(1)
        else:
            state="n/a"
            lot_size= 0
            signal.append(0)
        return total,state,lot_size,buy_arr,signal
        
    def sell(self,total,lot_size,price,signal,sell_arr):
        trade = price*lot_size
        fee = self.fee_rate*trade
        if fee < total + trade:
            total = total +trade -fee
            state = "n/a"
            signal.append(-1)
            sell_arr.append(trade)
        else:
            state = "buy"
            signal.append(0)
        return total,state,signal,sell_arr
    
    #needs validation to ensure it cannot be negative     
    def trades(self,rsi_signal,bband_signal,atr,rejection_signal,initial_money):
        total = initial_money
        total_arr = [total]
        state= "n/a"
        buys = []
        sells = []
        final_signal=[]
        relative_atr = atr/np.array(self.dataframe["Close/Last"])
        for i in range(1,len(rsi_signal)):
            current_price = self.dataframe["Close/Last"][i]
            current_position = 0
            
            if state == "n/a":
                if relative_atr[i-1]<0.04:
                    if (bband_signal[i-1]==2 or bband_signal[i-1]==1) or rejection_signal[i-1]==1:
                        #1% of total is an aggressive risk
                        risk = 0.02*total
                        if atr[i-1] == 0:
                            position_size = 0.0
                            final_signal.append(0)
                        else:
                            position_size = int(risk/(atr[i-1]*2))
                            max_alloc = 0.6
                            max_position = float((total * max_alloc) // current_price)
                            lot_size = min(position_size,max_position)
                            total,state,current_position,buys,final_signal = self.buy(total,lot_size,current_price,buys,final_signal)
                            buy_price = current_price
                    elif i>=30:
                        if self.fma[i-1]>self.sma[i-1]:
                            risk = 0.02*total
                            if atr[i-1] == 0:
                                position_size = 0.0
                                final_signal.append(0)
                            else:
                                position_size = int(risk/(atr[i-1]*2))
                                max_alloc = 0.4
                                max_position = float((total * max_alloc) // current_price)
                                lot_size = min(position_size,max_position)
                                total,state,current_position,buys,final_signal = self.buy(total,lot_size,current_price,buys,final_signal)
                                buy_price = current_price
                        else:
                            pass
                    
                        
                    else:
                        final_signal.append(0)
                elif relative_atr[i-1]<0.06:
                    if (bband_signal[i-1]==2 or bband_signal[i-1]==1)  and rejection_signal[i-1]==1:
                        #1% of total is an aggressive risk
                        risk = 0.02*total
                        if atr[i-1] == 0:
                            position_size = 0.0
                            final_signal.append(0)
                        else:
                            position_size = int(risk/(atr[i-1]*2))
                            max_alloc = 0.6
                            max_position = float((total * max_alloc) // current_price)
                            lot_size = min(position_size,max_position)
                            total,state,current_position,buys,final_signal = self.buy(total,lot_size,current_price,buys,final_signal)
                            buy_price = current_price
                    elif i>=30:
                        if self.fma[i-1]>self.sma[i-1]:
                            risk = 0.02*total
                            if atr[i-1] == 0:
                                position_size = 0.0
                                final_signal.append(0)
                            else:
                                position_size = int(risk/(atr[i-1]*2))
                                max_alloc = 0.4
                                max_position = float((total * max_alloc) // current_price)
                                lot_size = min(position_size,max_position)
                                total,state,current_position,buys,final_signal = self.buy(total,lot_size,current_price,buys,final_signal)
                                buy_price = current_price
                        else:
                            pass
                else:
                    final_signal.append(0)
            
            else:
                if relative_atr[i-1]>0.08:
                    position_size = current_position
                    total,state,final_signal,sells = self.sell(total,lot_size,current_price,final_signal,sells)
                elif (self.dataframe["Close/Last"][i] > buy_price + atr[i-1]*4) or self.dataframe["Close/Last"][i] < buy_price - atr[i-1]*2:
                    position_size = current_position
                    total,state,final_signal,sells = self.sell(total,lot_size,current_price,final_signal,sells)
                elif rejection_signal[i-1]==-1 or bband_signal[i-1]==-1:
                    position_size = current_position
                    total,state,final_signal,sells = self.sell(total,lot_size,current_price,final_signal,sells)
                    
                    
                else:
                    final_signal.append(0)
            total_arr.append(total)
        if state == "buy":
            position_size = current_position
            position_size = current_position
            total,state,final_signal,sells = self.sell(total,lot_size,current_price,final_signal,sells)
            total_arr.append(total)
            
        returns = np.diff(total_arr) / total_arr[:-1]  
        Sharpe_ratio = ((np.mean(returns)-0.02) / np.std(returns))
        stats_dict = {"Sharpe Ratio":Sharpe_ratio,
                      "Daily total": total_arr,
                      "rsi signal":rsi_signal,
                      "bollinger band signal": bband_signal,
                      "rejection signal": rejection_signal,
                      "overall signal":final_signal,
                      "bought":buys,
                      "sold":sells}
        return np.round(total,2),stats_dict
                
                        
                        
            
                    
    
    def backtest(self):
        rsi = self.relative_strength_index()
        ub,lb,ma = self.bollinger_bands()
        b_signal = self.bollinger_band_signal(ub,lb,ma)
        rs_signal = self.relative_strength_index_signal(rsi)
        average_true_range = self.Average_True()
        rejection_candles_sig = self.rejection_candles_signal(self.dataframe["Close/Last"],self.dataframe["High"],self.dataframe["Open"],self.dataframe["Low"])
        strat_total,stats_dict = self.trades(rs_signal,b_signal,average_true_range,rejection_candles_sig,100000)
        return strat_total,stats_dict
    
    

        
            
                
        