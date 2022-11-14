from utils import *
import os

api_key = 'b229374c-6819-4e1e-8403-69b1501d5c1e'

def main():
    ss = StockSymbol(api_key)
    current_dir = get_current_dir()
    
    # get spx list
    list_spx = ss.get_symbol_list(index="SPX")

    # get cac40 list
    list_cac40 = ss.get_symbol_list(index="PX1")

    spx_datas = {}
    for item in list_spx:
        symbol = item['symbol']
        try :
            spx_datas[symbol] = get_historical_datas(symbol, '1d')
        except Exception as err :
            list_spx.remove(item)
            continue

    dt = pd.DataFrame(columns = ['company','ticker','recommandation', 'date', 'traded price','actual price','wallet','pnl'])

    for item in list_spx :
        symbol = item['symbol']
        try :
            df = spx_datas[symbol].copy()
            myrow = strategy_macd(item, df)
            dt = pd.concat([dt,myrow])
        except Exception as err:
            continue
        
    week_ago = datetime.today() - timedelta(7)
    output = dt.loc[(dt['date'] > week_ago) & (dt['pnl'] > 0)].sort_values(by="pnl",ascending=False)
    output = output[['company','ticker','recommandation', 'date', 'traded price','actual price']]

    # order log
    output.to_csv(current_dir+'spx500_short_term_strat.csv',index=False)

    cac40_datas = {}
    for item in list_cac40:
        symbol = item['symbol']
        try :
            cac40_datas[symbol] = get_historical_datas(symbol, '1d')
        except Exception as err :
            list_cac40.remove(item)
            continue
        
    dt = pd.DataFrame(columns = ['company','ticker','recommandation', 'date', 'traded price','actual price','wallet','pnl'])

    for item in list_cac40:
        symbol = item['symbol']
        try :
            df = cac40_datas[symbol].copy()
            myrow = strategy_macd(item, df)
            dt = pd.concat([dt,myrow])
        except Exception as err:
            continue
        
    week_ago = datetime.today() - timedelta(7)
    output = dt.loc[(dt['date'] > week_ago) & (dt['pnl'] > 0)].sort_values(by="pnl",ascending=False)
    output = output[['company','ticker','recommandation', 'date', 'traded price','actual price']]

    # order log
    output.to_csv(current_dir+'cac40_short_term_strat.csv',index=False)

if __name__ == '__main__':
    main()