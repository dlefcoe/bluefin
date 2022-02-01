
'''

connect to server
execute query "to get ETF details"
paste all bonds from all ETF's into:
  [1] a single static file
  [2] a dated copy of the static file

with this list
  [1] generate list of unique bond isins
  [2] save unique list to static file
  [3] save unique list to dated file

also, with this list
  [1] generate list of unique etf isins
  [2] save unique list to static file
  [3] save unique list to dated file



'''

import time
import pyodbc
import pandas as pd


t0 = time.time()

conn = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=ht-srv1\SIMON,1434;'
    'Database=ETF_Fixed_Income;'
    'Trusted_Connection=yes;'
    )

cursor = conn.cursor()


t1 = time.time()
print('time taken to connect:', round(t1-t0, 1), 'seconds' )


print('running query...')
sql_string = "SELECT ETF_Component.Isin, ETF_Component.close_Issuer, ETF_Component.ETF_Isin, ETF_Component.Weight, ETF_Details.NAV, ETF_Details.NAV_Cur, ETF_Details.Cash_Component_Today, ETF_Details.Etf_min_basket, ETF_Details.Issuer, ETF_Component.accrued_interest \
    FROM ETF_type INNER JOIN ETF_Details ON ETF_type.Isin = ETF_Details.Isin INNER JOIN  ETF_Component ON ETF_Details.Isin = ETF_Component.ETF_Isin AND cast(ETF_Details.Etf_date as nvarchar) = cast(ETF_Component.Date_Component as nvarchar) \
    WHERE (ETF_Details.Etf_date = CONVERT(VARCHAR(12), GETDATE())) AND ( ETF_type.Type='Credit')"

df = pd.read_sql(sql_string, conn)

print(df)

t2 = time.time()
print('time taken run query:', round(t2-t1, 1), 'seconds' )

# save query to csv
folder_path = 'Y:\\DL_trade\\system_files\\'
file_name = 'bond_etf_convolution'
file_extension = '.csv'
full_path_file = folder_path + file_name + file_extension

df.to_csv(full_path_file)

print(f'the bond * etf file is here: {full_path_file}')

# unique bonds
unique_list = df['Isin'].unique()
unique_list_df = pd.DataFrame({'isin':unique_list})
print('\n\nunique bond list:')
print(unique_list_df)

# write unique bonds to file
folder_path = 'Y:\\DL_trade\\system_files\\'
file_name = 'unique_bonds'
file_extension = '.csv'
full_path_file = folder_path + file_name + file_extension
unique_list_df.to_csv(full_path_file)
print()
print(f'the unique bond isin file is here: {full_path_file}')

# unique etf's
unique_etf_list = df['ETF_Isin'].unique()
unique_etf_df = pd.DataFrame({'isin':unique_etf_list})
print('\n\nunique etf list:')
print(unique_etf_df)

# write unique etfs to file
folder_path = 'Y:\\DL_trade\\system_files\\'
file_name = 'unique_etfs'
file_extension = '.csv'
full_path_file = folder_path + file_name + file_extension
unique_etf_df.to_csv(full_path_file)
print()
print(f'the unique etf isin file is here: {full_path_file}')

# unique currency pairs
# not enough info


