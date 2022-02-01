'''

price PFC from first principals

'''

# standard imports
import os
import time
import datetime as dt
import pandas as pd
import numpy as np
import threading


# import internal modules
import pcf_support
import subscribe_to_bonds


# list of isins that are not percentages
factor_100 = pcf_support.factor_100


def main():
    ''' the main module: all other code is run from here. No arguments. '''

    # current date
    today = dt.datetime.today()
    prev_work_day = today - pd.tseries.offsets.BDay(1) # previous business day
    current_date_yyyymmdd = dt.datetime.today().strftime('%Y%m%d')
    prev_date_ddmmyy = prev_work_day.strftime('%d%m%y')
    # pcf_ubs(current_date_yyyymmdd)
    ticker = 'ieac'  #ieac'

    # run ishares
    t0 = time.time()
    r = pcf_ishares(current_date_yyyymmdd, prev_date_ddmmyy, ticker, calc_type='static')
    print('nav result:', r)
    t1 = time.time()
    print('time taken:', round(t1-t0, 2), 'seconds')

    # invoke live data
    # subscribe_to_bonds.subscribe_to_list(r['isin_list'])
    print('subscribing to live: wait 10 seconds')
    thr = threading.Thread(target=subscribe_to_bonds.subscribe_to_list, args=([r['isin_list']]) )
    thr.start()
    time.sleep(10)

    # run process every 10 seconds
    for i in range(100):
        threading.Timer(interval= 10 *(i+1), function=pcf_ishares,args= [current_date_yyyymmdd, prev_date_ddmmyy, ticker],kwargs={'calc_type':'live'}).start()

        # r_live = pcf_ishares(current_date_yyyymmdd, prev_date_ddmmyy, ticker, calc_type='live')
        # print('live nav:', r_live['nav_per_share'])


def pcf_ishares(current_date_yyyymmdd, prev_date_ddmmyy, ticker, calc_type='static'):
    '''
    module for ishares

    inputs:
        current_date_yyyymmdd (str): a formatted current date
        prev_date_ddmmyy (str): a formatted previous date
        ticker (str): the etf ticker
        type (str):
            static: for last nights close reconciliation    
            live: for live pub-sub data
    
    returns:
        fair value for nav

    '''

    # get pcf for ishares
    pcf_folder_base = 'Y:\\Benjamin\\Market_Making\\PCFs\\ishares_Bonds\\'
    pcf_folder_base = pcf_folder_base + current_date_yyyymmdd + "\\"
    pcf_file_name = "CPCF" + ticker + prev_date_ddmmyy + "A.csv"
    pcf_full_path = pcf_folder_base + pcf_file_name


    # check if file exists
    if os.path.isfile(pcf_full_path):
        print('opening file:', pcf_full_path)
    else:
        print(f'file does not exist: {pcf_full_path}')
        return 'no file found'



    # determine start of asset list by reading first column of csv
    # "Estimated Cash Component:" defines start of the main table
    # "Fx Rates" defines the end of the main table
    try:
        #read first 7 columns of csv into dataframe
        df_raw = pd.read_csv(pcf_full_path, index_col=None, names = list(range(7)))
        df_raw = pd.DataFrame(df_raw)
    except:
        print('error reading file for ticker:', ticker)
        return f'error reading file for ticker: {ticker}'
    
    start_row = df_raw[df_raw[0] == 'Estimated Cash Component:'].index[0] + 1
    end_row = df_raw[df_raw[0] == 'Fx Rates'].index[0] - 1
    #number_of_rows = end_row - start_row


    try:
        # create new dataframe from the raw data
        df = pd.DataFrame(df_raw[ start_row: end_row])
        df.columns=['isin', 'long name', 'coupon', 'maturity', 'amount', 'clean price', 'acc int']
        print(f'data read: {len(df)} assets from {len(df_raw)} raw data')
    except:
        print('error reading file for ticker:', ticker)
        return f'error reading file for ticker: {ticker}'
    
    # convert text in relevant columns to numbers
    df[['coupon']] = df[['coupon']].apply(pd.to_numeric)
    df[['amount','clean price', 'acc int']] = df[['amount','clean price', 'acc int']].apply(pd.to_numeric)
    
    # if isin is in the list to be multiplied by 100
    df['factor 100'] = np.where(df['isin'].isin(factor_100), 100, 1)

    # use either closing (static) or live prices
    if calc_type=='static':
        print('computing static value')
    elif calc_type=='live':
        # subscribe to live data
        print('using live data')
        # df['clean price'] = subscribe_to_bonds.bond_values.values()
        
        # turn dict into dataframe
        df_live_prices = pd.DataFrame().from_dict(subscribe_to_bonds.bond_values, orient='index')
        df_live_prices.reset_index(level=0, inplace=True)
        df_live_prices.columns = ['isin','clean price']
        df_live_prices[['isin','the type']] = pd.DataFrame(df_live_prices['isin'].tolist(), index=df_live_prices.index)

        df_live_prices['clean price'].replace('', 100, inplace=True)
        df_live_prices['clean price']=df_live_prices['clean price'].astype(float)
        
        # replace clean 
        df = df.merge(df_live_prices,  on='isin', how='left')
        df['clean price'] = df['clean price_y']
        df.drop(['clean price_x'], axis=1, inplace=True)
        df.drop(['clean price_y'], axis=1, inplace=True)
        print(df.describe())


    # sum products to work out asset values 
    df['asset vals'] = df['amount'] * (df['clean price'] + df['acc int'])/100 * df['factor 100']
    sum_assets = sum(df['asset vals'])

    print('items with factor 100:')
    c = df[df['factor 100']==100]
    print(c)

    sum_funds = 0 # funds taken care of with factor 100

    # Share Class Ratio:
    share_class_ratio = float(df_raw.loc[df_raw[0]=='Share Class Ratio:'][1])
    if np.isnan(share_class_ratio): share_class_ratio = 1
    print('share class ratio',share_class_ratio)


    all_cash = float(df_raw.loc[df_raw[0]=='Confirmed Cash Component:'][1])
    print(f'all cash: {all_cash}')

    all_futures = 0

    nav = sum_assets*share_class_ratio  + all_cash + all_futures
    
    # Shares In Issue:
    number_shares = float(df_raw.loc[df_raw[0]=='Shares In Issue:'][1])

    nav_per_share = nav / number_shares

    # closing nav (Total NAV per share:)
    closing_nav_per_share = float(df_raw.loc[df_raw[0]=='Total NAV per share:'][1])

    nav_error_bps = (nav_per_share / closing_nav_per_share - 1) * 10000

    # print(df)
    nav_returns = {
        'nav_per_share':nav_per_share, 
        'closing_nav_per_share':closing_nav_per_share,
        'nav_error_bps':nav_error_bps,
        'isin_list': df['isin']
        }
    file_output = 'Y:\DL_trade\code\python\pcf calculator\pcf_output.txt'

    with open(file_output, "a") as f:
        f.write(f'nav per share {nav_returns}  \n')

    print(nav_returns['nav_per_share'])

    return nav_returns



def pcf_ubs(current_date_yyyymmdd):
    # get pcf (for ubs)
    pcf_folder_base = 'Y:\\Benjamin\\Market_Making\\PCFs\\UBS_Bonds\\'
    pcf_folder_base = pcf_folder_base + current_date_yyyymmdd + "\\"
    pcf_file_name = "CBUS5E_" + current_date_yyyymmdd + ".csv"
    pcf_full_path = pcf_folder_base + pcf_file_name

    print('opening file:')
    print(pcf_full_path)

    # read pcf
    start_row = 20
    end_row = 100

    try:
        df = pd.read_csv(pcf_full_path,  skiprows=start_row, 
                        header=start_row+1, nrows=(end_row-start_row))
        print('data read')
    except:
        print('error reading file')
        quit()
        

    print(df)
    return 100



if __name__=="__main__":
    main()

