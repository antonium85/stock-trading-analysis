from utils import *
import os

def apply_strategy(list_companies, data, func) :
    print('Apply strategy for ',func)
    dt = pd.DataFrame(columns = ['company','ticker','recommandation', 'date', 'traded price','actual price','wallet','pnl','take profit','stop loss'])

    for index,row in list_companies.iterrows():
        symbol = row['symbol']
        try :
            myrow = func(row, df=data[symbol].copy())
            dt = pd.concat([dt,myrow])
        except Exception as err:
            print(symbol,err)
            continue
        
    week_ago = datetime.today() - timedelta(7)
    output = dt.loc[(dt['date'] > week_ago) & (dt['pnl'] > 0)].sort_values(by="pnl",ascending=False)
    output = output[['company','ticker','recommandation', 'date', 'traded price','actual price','pnl','take profit','stop loss']]

    return output

def main():
    current_dir = get_current_dir()
    
    # get spx list
    list_spx = pd.read_csv(current_dir+'markets/SPX500.csv')

    # get spf120 list
    list_spf120 = pd.read_csv(current_dir+'markets/SPF120.csv')
    
    print('Update results for SPX500')
    spx_datas = {}
    for index,row in list_spx.iterrows():
        symbol = row['symbol']
        try :
            spx_datas[symbol] = get_historical_datas(symbol, '1d')
        except Exception as err :
            continue

    # short-term strategy for SPX500
    output = apply_strategy(list_spx,spx_datas,strategy_macd)
    # order log
    output.to_csv(current_dir+'spx500_short_term_strat.csv',index=False)

    # mid-term strategy for SPX500
    output = apply_strategy(list_spx,spx_datas,strategy_sma50vs100)
    # order log
    output.to_csv(current_dir+'spx500_mid_term_strat.csv',index=False)

    # long-term strategy for SPX500
    output = apply_strategy(list_spx,spx_datas,strategy_sma100vs200)
    # order log
    output.to_csv(current_dir+'spx500_long_term_strat.csv',index=False)
    
    print('Update results for SPF120')
    spf120_datas = {}
    for index,row in list_spf120.iterrows():
        symbol = row['symbol']
        try :
            spf120_datas[symbol] = get_historical_datas(symbol, '1d')
        except Exception as err :
            print(err)
            continue
    
    # short-term strategy for SPF120
    output = apply_strategy(list_spf120,spf120_datas,strategy_macd)
    # order log
    output.to_csv(current_dir+'spf120_short_term_strat.csv',index=False)

    # short-term strategy for SPF120
    output = apply_strategy(list_spf120,spf120_datas,strategy_sma50vs100)
    # order log
    output.to_csv(current_dir+'spf120_mid_term_strat.csv',index=False)

    # long-term strategy for SPF120
    output = apply_strategy(list_spf120,spf120_datas,strategy_sma100vs200)
    # order log
    output.to_csv(current_dir+'spf120_long_term_strat.csv',index=False)

if __name__ == '__main__':
    main()