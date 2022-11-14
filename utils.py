import ta
import yfinance as yf
from datetime import datetime, timedelta
import time
import pandas as pd
from stocksymbol import StockSymbol

api_key = 'b229374c-6819-4e1e-8403-69b1501d5c1e'

def get_sp500_symbol_list():
    ss = StockSymbol(api_key)
    
    # get symbol list based on index
    symbol_list_spx = ss.get_symbol_list(index="SPX")

    return symbol_list_spx

def get_historical_datas(ticker, interval):
  if interval == '1d':
    end_date = datetime.today()
  elif interval == '1wk':
    end_date = datetime.today() #- timedelta(1)
  start_date = '2010-01-01' #end_date - timedelta(365*10)

  df = yf.download(ticker, start=start_date, end=end_date.strftime('%Y-%m-%d'), interval=interval, keepna=True, progress=False, show_errors=False)

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
      
      lastIndex = index
      lastPosition = 'sell'
      lastPrice = row['Close']

  finalResult = usd + share * df['Close'].iloc[-1]
  pnl = (finalResult - 1000)/1000 * 100

  myrow = pd.DataFrame({'company':item['longName'],'ticker':item['symbol'],'recommandation':lastPosition,'date':lastIndex,'traded price':lastPrice,'actual price':df['Close'].iloc[-1],'wallet':finalResult,'pnl':pnl,'tp':df['TP'].iloc[-1],'sl':df['SL'].iloc[-1]},index=[item['symbol']])

  return myrow

def strategy_sma100vs200(item, df=pd.DataFrame()):
  lastPosition=''
  lastIndex = ''
  lastPrice = ''

  usd = 1000
  share = 0

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
      
      lastIndex = index
      lastPosition = 'sell'
      lastPrice = row['Close']

  finalResult = usd + share * df['Close'].iloc[-1]
  pnl = (finalResult - 1000)/1000 * 100

  myrow = pd.DataFrame({'company':item['longName'],'ticker':item['symbol'],'recommandation':lastPosition,'date':lastIndex,'traded price':lastPrice,'actual price':df['Close'].iloc[-1],'wallet':finalResult,'pnl':pnl,'tp':df['TP'].iloc[-1],'sl':df['SL'].iloc[-1]},index=[item['symbol']])

  return myrow

def strategy_macd(item, df=pd.DataFrame()):
  lastPosition=''
  lastIndex = ''
  lastPrice = ''

  usd = 1000
  share = 0

  for index, row in df.iterrows():
    if row['MACD_DIFF'] > 0 and usd > 10:
      share = usd / row['Close']
      usd = 0
      
      lastIndex = index
      lastPosition = 'buy'
      lastPrice = row['Close']

    if row['MACD_DIFF'] < 0 and share > 1:
      usd = share * row['Close']
      share = 0
      
      lastIndex = index
      lastPosition = 'sell'
      lastPrice = row['Close']

  finalResult = usd + share * df['Close'].iloc[-1]
  pnl = (finalResult - 1000)/1000 * 100

  myrow = pd.DataFrame({'company':item['longName'],'ticker':item['symbol'],'recommandation':lastPosition,'date':lastIndex,'traded price':lastPrice,'actual price':df['Close'].iloc[-1],'wallet':finalResult,'pnl':pnl,'tp':df['TP'].iloc[-1],'sl':df['SL'].iloc[-1]},index=[item['symbol']])

  return myrow