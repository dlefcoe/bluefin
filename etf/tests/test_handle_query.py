


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

print(type(cursor))

t1 = time.time()
print('time taken to connect:', round(t1-t0, 1), 'seconds' )


cursor.execute(
    "SELECT ETF_Component.Isin, ETF_Component.close_Issuer, ETF_Component.ETF_Isin, ETF_Component.Weight, ETF_Details.NAV, ETF_Details.NAV_Cur, ETF_Details.Cash_Component_Today, ETF_Details.Etf_min_basket, ETF_Details.Issuer, ETF_Component.accrued_interest \
    FROM ETF_type INNER JOIN ETF_Details ON ETF_type.Isin = ETF_Details.Isin INNER JOIN  ETF_Component ON ETF_Details.Isin = ETF_Component.ETF_Isin AND cast(ETF_Details.Etf_date as nvarchar) = cast(ETF_Component.Date_Component as nvarchar) \
    WHERE (ETF_Details.Etf_date = CONVERT(VARCHAR(12), GETDATE())) AND ( ETF_type.Type='Credit')"
    )


t2 = time.time()
print('time taken to execute query:', round(t2-t1, 1), 'seconds' )

result = [row for row in cursor]

t3 = time.time()
print('time taken to populate list:', round(t3-t2, 1), 'seconds' )

df = pd.DataFrame.from_records(result)
df.columns = ['bond isin', 'bond close', 'etf isin', 'weight', 'etf nav' ,'nav ccy', 'cash component', 'etf min basket', 'etf issuer', 'bond acc int']


t4 = time.time()
print('list to dataframe:', round(t4-t3, 1), 'seconds' )
print()

print(df)



# method 2
print('trying method 2')
sql_string = "SELECT ETF_Component.Isin, ETF_Component.close_Issuer, ETF_Component.ETF_Isin, ETF_Component.Weight, ETF_Details.NAV, ETF_Details.NAV_Cur, ETF_Details.Cash_Component_Today, ETF_Details.Etf_min_basket, ETF_Details.Issuer, ETF_Component.accrued_interest \
    FROM ETF_type INNER JOIN ETF_Details ON ETF_type.Isin = ETF_Details.Isin INNER JOIN  ETF_Component ON ETF_Details.Isin = ETF_Component.ETF_Isin AND cast(ETF_Details.Etf_date as nvarchar) = cast(ETF_Component.Date_Component as nvarchar) \
    WHERE (ETF_Details.Etf_date = CONVERT(VARCHAR(12), GETDATE())) AND ( ETF_type.Type='Credit')"
df2 = pd.read_sql(sql_string, conn)

print(df2)
# print(result2)

