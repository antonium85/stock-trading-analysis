import ta
import yfinance as yf
from datetime import datetime, timedelta
import time
import pandas as pd
import os

def get_current_dir():
    full_path = os.path.realpath(__file__)
    return os.path.dirname(full_path) + '/'

def precision(x):
    return float("{:.2f}".format(x))

def get_historical_datas(ticker, interval):
  if interval == '1d':
    end_date = datetime.today()
  elif interval == '1wk':
    end_date = datetime.today() #- timedelta(1)
  start_date = '2010-01-01' #end_date - timedelta(365*10)

  df = yf.download(ticker, start=start_date, end=end_date.strftime('%Y-%m-%d'), interval=interval, progress=False, show_errors=False)

  df['Close'] = pd.to_numeric(df['Close'])
  df['High'] = pd.to_numeric(df['High'])
  df['Low'] = pd.to_numeric(df['Low'])
  df['Open'] = pd.to_numeric(df['Open'])

  del(df['Volume'])
  del(df['Adj Close'])

  # sma
  df['SMA5'] = ta.trend.sma_indicator(df['Close'], 5)
  df['SMA8'] = ta.trend.sma_indicator(df['Close'], 8)
  df['SMA13'] = ta.trend.sma_indicator(df['Close'], 13)
  df['SMA50'] = ta.trend.sma_indicator(df['Close'], 50)
  df['SMA100'] = ta.trend.sma_indicator(df['Close'], 100)
  df['SMA200'] = ta.trend.sma_indicator(df['Close'], 200)

  # ema
  df['EMA8'] = ta.trend.sma_indicator(df['Close'], 8)
  df['EMA21'] = ta.trend.sma_indicator(df['Close'], 21)
  df['EMA50'] = ta.trend.sma_indicator(df['Close'], 50)

  # macd
  df['MACD'] = ta.trend.macd(df['Close'])
  df['MACD_SIGNAL'] = ta.trend.macd_signal(df['Close'])
  df['MACD_DIFF'] = ta.trend.macd_diff(df['Close'])

  df['TENKAN'] = ta.trend.ichimoku_conversion_line(df['High'],df['Low'])
  df['KIJUN'] = ta.trend.ichimoku_base_line(df['High'],df['Low'])
  df['SSA'] = ta.trend.ichimoku_a(df['High'],df['Low']).shift(periods=26)
  df['SSB'] = ta.trend.ichimoku_b(df['High'],df['Low']).shift(periods=26)

  df['TR'] = [max(tup) for tup in list(zip(df['High'] - df['Low'],
                                        (df['High'] - df['Close'].shift()).abs(),
                                        (df['Low']  - df['Close'].shift()).abs()))]
  df['ATR'] = df['TR'].rolling(14).sum()/14

  df['TP'] = df['ATR'] * 3
  df['SL'] = df['ATR'] * 2

  del(df['TR'])
  del(df['ATR'])

  return df

def strategy_sma50vs100(item, df=pd.DataFrame()):
    lastPosition=''
    lastIndex = ''
    lastPrice = ''

    usd = 1000
    share = 0

    nbTrade = 0
    goodTrade = 0
    winrate = 0

    for index, row in df.iterrows():
        if row['SMA50'] > row['SMA100'] and usd > 10:
            share = usd / row['Close']
            usd = 0
            
            lastIndex = index
            lastPosition = 'buy'
            lastPrice = row['Close']

        if row['SMA50'] < row['SMA100'] and share > 1:
            usd = share * row['Close']
            share = 0
            
            nbTrade += 1
            if row['Close'] > lastPrice : goodTrade += 1

            lastIndex = index
            lastPosition = 'sell'
            lastPrice = row['Close']

    finalResult = usd + share * df['Close'].iloc[-1]
    pnl = (finalResult - 1000)/1000 * 100
    tp = lastPrice + df['TP'].iloc[-1]
    sl = lastPrice - df['SL'].iloc[-1]
    if nbTrade > 0 : 
        winrate = goodTrade/nbTrade * 100
    
    myrow = pd.DataFrame({'company':item['name'],'ticker':item['symbol'],'recommandation':lastPosition,'date':lastIndex,'traded price':lastPrice,'actual price':df['Close'].iloc[-1],'wallet':finalResult,'pnl':pnl,'win rate':winrate,'take profit':tp,'stop loss':sl},index=[item['symbol']])
    
    return myrow

def strategy_sma5vs8vs13(item, df=pd.DataFrame()):
    lastPosition=''
    lastIndex = ''
    lastPrice = ''

    usd = 1000
    share = 0

    nbTrade = 0
    goodTrade = 0
    winrate = 0

    for index, row in df.iterrows():
        if row['SMA5'] > row['SMA13'] and row['SMA8'] > row['SMA13'] and usd > 10:
            share = usd / row['Close']
            usd = 0
            
            lastIndex = index
            lastPosition = 'buy'
            lastPrice = row['Close']

        if row['SMA5'] < row['SMA13'] and row['SMA8'] < row['SMA13'] and share > 1:
            usd = share * row['Close']
            share = 0

            nbTrade += 1
            if row['Close'] > lastPrice : goodTrade += 1
            
            lastIndex = index
            lastPosition = 'sell'
            lastPrice = row['Close']

    finalResult = usd + share * df['Close'].iloc[-1]
    pnl = (finalResult - 1000)/1000 * 100
    tp = lastPrice + df['TP'].iloc[-1]
    sl = lastPrice - df['SL'].iloc[-1]
    if nbTrade > 0 : 
        winrate = goodTrade/nbTrade * 100
    
    myrow = pd.DataFrame({'company':item['name'],'ticker':item['symbol'],'recommandation':lastPosition,'date':lastIndex,'traded price':lastPrice,'actual price':df['Close'].iloc[-1],'wallet':finalResult,'pnl':pnl,'win rate':winrate,'take profit':tp,'stop loss':sl},index=[item['symbol']])
    
    return myrow

def strategy_ema8vs21vs50(item, df=pd.DataFrame()):
    lastPosition=''
    lastIndex = ''
    lastPrice = ''

    usd = 1000
    share = 0

    nbTrade = 0
    goodTrade = 0
    winrate = 0

    for index, row in df.iterrows():
        if row['EMA8'] > row['EMA50'] and row['EMA21'] > row['EMA50'] and usd > 10:
            share = usd / row['Close']
            usd = 0
            
            lastIndex = index
            lastPosition = 'buy'
            lastPrice = row['Close']

        if row['EMA8'] < row['EMA50'] and row['EMA21'] < row['EMA50'] and share > 1:
            usd = share * row['Close']
            share = 0

            nbTrade += 1
            if row['Close'] > lastPrice : goodTrade += 1
            
            lastIndex = index
            lastPosition = 'sell'
            lastPrice = row['Close']

    finalResult = usd + share * df['Close'].iloc[-1]
    pnl = (finalResult - 1000)/1000 * 100
    tp = lastPrice + df['TP'].iloc[-1]
    sl = lastPrice - df['SL'].iloc[-1]
    if nbTrade > 0 : 
        winrate = goodTrade/nbTrade * 100
    
    myrow = pd.DataFrame({'company':item['name'],'ticker':item['symbol'],'recommandation':lastPosition,'date':lastIndex,'traded price':lastPrice,'actual price':df['Close'].iloc[-1],'wallet':finalResult,'pnl':pnl,'win rate':winrate,'take profit':tp,'stop loss':sl},index=[item['symbol']])

    return myrow

def strategy_sma100vs200(item, df=pd.DataFrame()):
    lastPosition=''
    lastIndex = ''
    lastPrice = ''

    usd = 1000
    share = 0

    nbTrade = 0
    goodTrade = 0
    winrate = 0

    for index, row in df.iterrows():
        if row['SMA100'] > row['SMA200'] and usd > 10:
            share = usd / row['Close']
            usd = 0
            
            lastIndex = index
            lastPosition = 'buy'
            lastPrice = row['Close']

        if row['SMA100'] < row['SMA200'] and share > 1:
            usd = share * row['Close']
            share = 0

            nbTrade += 1
            if row['Close'] > lastPrice : goodTrade += 1
            
            lastIndex = index
            lastPosition = 'sell'
            lastPrice = row['Close']

    finalResult = precision(usd + share * df['Close'].iloc[-1])
    pnl = (finalResult - 1000)/1000 * 100
    tp = precision(lastPrice + df['TP'].iloc[-1])
    sl = precision(lastPrice - df['SL'].iloc[-1])
    if nbTrade > 0 : 
        winrate = goodTrade/nbTrade * 100
    
    myrow = pd.DataFrame({'company':item['name'],'ticker':item['symbol'],'recommandation':lastPosition,'date':lastIndex,'traded price':lastPrice,'actual price':df['Close'].iloc[-1],'wallet':finalResult,'pnl':pnl,'win rate':winrate,'take profit':tp,'stop loss':sl},index=[item['symbol']])
    return myrow

def strategy_macd(item, df=pd.DataFrame()):
    lastPosition=''
    lastIndex = ''
    lastPrice = 0

    usd = 1000
    share = 0

    nbTrade = 0
    goodTrade = 0

    for index, row in df.iterrows():
        if row['MACD_DIFF'] > 0 and (row['Close'] > row['SSA'] and row['Close'] > row['SSB']) and usd > 10:
            share = usd / row['Close']
            usd = 0
            
            lastIndex = index
            lastPosition = 'buy'
            lastPrice = row['Close']

        if (row['MACD_DIFF'] < 0 and row['Close'] < row['SSA'] and row['Close'] < row['SSB']) and share > 1:
            usd = share * row['Close']
            share = 0

            nbTrade += 1
            if row['Close'] > lastPrice : goodTrade += 1 
            
            lastIndex = index
            lastPosition = 'sell'
            lastPrice = row['Close']

    finalResult = usd + share * df['Close'].iloc[-1]
    pnl = (finalResult - 1000)/1000 * 100
    tp = lastPrice + df['TP'].iloc[-1]
    sl = lastPrice - df['SL'].iloc[-1]

    myrow = pd.DataFrame({'company':item['name'],'ticker':item['symbol'],'recommandation':lastPosition,'date':lastIndex,'traded price':lastPrice,'actual price':df['Close'].iloc[-1],'wallet':finalResult,'pnl':pnl,'win rate':goodTrade/nbTrade*100,'take profit':tp,'stop loss':sl},index=[item['symbol']])

    return myrow