from utils import *
import os

def main():
    current_dir = get_current_dir()
    
    # get spx list
    list_spx = pd.read_csv(current_dir+'markets/SPX500.csv')

    # get spf120 list
    list_spf120 = pd.read_csv(current_dir+'markets/SPF120.csv')

    spx_datas = {}
    for index,row in list_spx.iterrows():
        symbol = row['symbol']
        try :
            spx_datas[symbol] = get_historical_datas(symbol, '1d')
        except Exception as err :
            continue

    dt = pd.DataFrame(columns = ['company','ticker','recommandation', 'date', 'traded price','actual price','wallet','pnl','take profit','stop loss'])

    for index,row in list_spx.iterrows() :
        symbol = row['symbol']
        try :
            df = spx_datas[symbol].copy()
            myrow = strategy_macd(row, df)
            dt = pd.concat([dt,myrow])
        except Exception as err:
            continue
        
    week_ago = datetime.today() - timedelta(7)
    output = dt.loc[(dt['date'] > week_ago) & (dt['pnl'] > 0)].sort_values(by="pnl",ascending=False)
    output = output[['company','ticker','recommandation', 'date', 'traded price','actual price','take profit','stop loss']]

    # order log
    output.to_csv(current_dir+'spx500_short_term_strat.csv',index=False)

    spf120_datas = {}
    for index,row in list_spf120.iterrows():
        symbol = row['symbol']
        try :
            spf120_datas[symbol] = get_historical_datas(symbol, '1d')
        except Exception as err :
            continue
        
    dt = pd.DataFrame(columns = ['company','ticker','recommandation', 'date', 'traded price','actual price','wallet','pnl','take profit','stop loss'])

    for index,row in list_spf120.iterrows():
        symbol = row['symbol']
        try :
            df = spf120_datas[symbol].copy()
            myrow = strategy_macd(row, df)
            dt = pd.concat([dt,myrow])
        except Exception as err:
            continue
        
    week_ago = datetime.today() - timedelta(7)
    output = dt.loc[(dt['date'] > week_ago) & (dt['pnl'] > 0)].sort_values(by="pnl",ascending=False)
    output = output[['company','ticker','recommandation', 'date', 'traded price','actual price','take profit','stop loss']]

    # order log
    output.to_csv(current_dir+'spf120_short_term_strat.csv',index=False)

if __name__ == '__main__':
    main()