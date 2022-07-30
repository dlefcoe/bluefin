# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 09:04:50 2021

@author: Keith Wynroe
"""


import os
import math
import pandas as pd
import numpy as np
from collections import defaultdict
from scipy.sparse import csr_matrix

pcf_path = "Y:\\Benjamin\\Market_Making\\PCFs\\ISHARES_Bonds\\20211213\\"



ls = ["IE00BK8MB266",
"IE00B9346255",
"IE00B50QMP13",
"IE00BK8M8R05",
"MX0MGO000003",
"MX0MGO000078",
"MX0MGO0000D8",
"MX0MGO0000H9",
"MX0MGO0000J5",
"MX0MGO0000B2",
"MX0MGO0000P2",
"MX0MGO0000Q0",
"MX0MGO0000R8",
"MX0MGO0000U2",
"MX0MGO0000Y4",
"MX0MGO000102",
"MX0MGO000128",
"MX0MGO000151",
"MX0MGO0001C8",
"IE00BMC7BF44",
"BRSTNCLTN7O0",
"BRSTNCLTN7Q5",
"BRSTNCLTN7S1",
"BRSTNCLTN7W3",
"BRSTNCNTF147",
"BRSTNCNTF170",
"BRSTNCNTF1P8",
"BRSTNCNTF1Q6",
"BRSTNCNTF204"
]

def share_ratios(row):
    if row.name in ls:
        return 100

    else:
        return 1

x = 10
print('hello')

cash_dct = {}
price_dct  = {}
share_dct = {}

def reconcile(file):
    adj_bp_diff = float('inf')
    df = pd.read_csv(pcf_path + file, index_col = "isin", names = ["isin", "country", "coupon", "maturity", "quantity", "price", "accrued int", "original face"])
    nav = float(df.loc["Total NAV per share:", "country"])
    cash = float(df.loc["Confirmed Cash Component:", "country"])
    shares = float(df.loc["Shares In Issue:", "country"])
    if "Share Class Ratio:" in df.index.tolist():
        scr = float(df.loc["Share Class Ratio:", "country"])
        if math.isnan(scr):
            scr = 1
    bonds = df[df.price.notnull()]
    bonds["share_ratio"] = bonds.apply(lambda row: share_ratios(row), axis = 1)
    bonds["quantity"] = [float(x) for x in bonds["quantity"]]
    bonds["price"] = [float(x) for x in bonds["price"]]
    bonds["accrued int"] = [float(x) for x in bonds["accrued int"]]
    min_bask = float(df.loc["Min Basket Size:", "country"]) 
    if math.isnan(min_bask):
        min_bask = shares
    bonds["dirty_price"] = bonds["quantity"] * (bonds["price"] + bonds["accrued int"])
    nav_calc = (((sum(bonds["dirty_price"]*bonds["share_ratio"]))*.01)*scr + cash)/shares
    bp_diff = (nav/nav_calc-1)*10000
    if abs(bp_diff) > 0.1:
        adj_nav = nav_calc * shares/min_bask
        adj_bp_diff = (nav/adj_nav-1)*10000
    return nav, bp_diff, adj_bp_diff

file_list = []
err = []
ok_list = []
dct = defaultdict(int)
m_list = []
for file in os.listdir(pcf_path):
    file_list.append(file)
    
    if file.endswith(".csv") and file.startswith("CPCF"):
        
        try:
            a,b,c= reconcile(file)
            ok_list.append(file)
            print(a,b,c)
            if min(abs(b),abs(c)) < 0.1:
                dct["success"] += 1
                m_list.append(file)
            else:
                dct["off"]  += 1
                err.append(file)
                m_list.append(file)

                
        except KeyboardInterrupt:
            break
        except Exception as e:
            
            dct[str(e)[:10]] += 1
  
print(dct)

def price(weights, prices, scr, cash, shares, adj_arr):
    raw = weights.dot(np.multiply(prices, adj_arr)*.01)
    ans  = np.multiply(raw, scr)
    ans += cash
    return np.multiply(ans, (1/shares))

etf_name = file.split(".")[0]
temp = pd.read_csv(pcf_path + file, index_col = "isin", names = ["isin", "country", "coupon", "maturity", "quantity", "price", "accrued int", "original face"])
cash = float(temp.loc["Confirmed Cash Component:", "country"])
shares = float(temp.loc["Shares In Issue:", "country"])
if "Share Class Ratio:" in df.index.tolist():
    scr = float(df.loc["Share Class Ratio:", "country"])
    if math.isnan(scr):
        scr = 1
shares[etf_name] = shares
cash[etf_name] = cash
scr[etf_name] = scr

import numpy as np

def random_walk_2D(sim_steps):
    """ Walk on 2D unit steps
        return  x_sim, y_sim, trajectory, number_of_steps_first_hit to y=1-x """
    random_moves_x = np.insert(np.random.choice([1,0,-1], sim_steps), 0, 0)
    random_moves_y = np.insert(np.random.choice([1,0,-1], sim_steps), 0, 0)
    x_sim = np.cumsum(random_moves_x)
    y_sim = np.cumsum(random_moves_y)
    trajectory = np.array((x_sim,y_sim)).T
    y_hat = 1-x_sim # checking if hit y=1-x
    y_hit = y_hat-y_sim
    hit_steps = np.where(y_hit == 0)
    number_of_steps_first_hit = -1
    if hit_steps[0].shape[0] > 0:
        number_of_steps_first_hit = hit_steps[0][0]
    return x_sim, y_sim, trajectory, number_of_steps_first_hit

for file in m_list:
    etf_name = file.split(".")[0]
    temp = pd.read_csv(path + file, index_col = "isin", names = ["isin", "country", "coupon", "maturity", "quantity", "price", "accrued int", "original face"])
    cash = float(temp.loc["Confirmed Cash Component:", "country"])
    shares = float(temp.loc["Shares In Issue:", "country"])
    if "Share Class Ratio:" in temp.index.tolist():
        scr = float(temp.loc["Share Class Ratio:", "country"])
        if math.isnan(scr):
            scr = 1
    cash_dct[etf_name] = cash
    share_dct[etf_name] = shares
    scr_dct[etf_name] = scr
    temp["etf_name"] = etf_name
    temp = temp.reset_index()
    bonds = temp[(temp.price.notnull()) & (temp["isin"].notnull())]
    bonds["quantity"] = [float(x) for x in bonds["quantity"]]
    bonds["price"] = [float(x) for x in bonds["price"]]
    bonds["accrued int"] = [float(x) for x in bonds["accrued int"]]
    bonds["dirty_price"] = (bonds["price"] + bonds["accrued int"])
    bonds = bonds.set_index(["etf_name", "isin"])
    df = df.append(bonds)


for file in m_list:
    etf_name = file.split(".")[0]
    bonds = pd.read_csv(pcf_path + file, index_col = "isin", names = ["isin", "country", "coupon", "maturity", "quantity", "price", "accrued int", "original face"])
    bonds["dirty_price"] = (bonds["price"] + bonds["accrued int"])
    cash = float(bonds.loc["Confirmed Cash Component:", "country"])
    shares = float(bonds.loc["Shares In Issue:", "country"])
    if "Share Class Ratio:" in bonds.index.tolist():
        scr = float(bonds.loc["Share Class Ratio:", "country"])
        if math.isnan(scr):
            scr = 1
    bonds = bonds[bonds.price.notnull()]
    cash_dct[etf_name] = cash
    share_dct[etf_name] = shares
    scr_dct[etf_name] = scr
    for idx in bonds.index.tolist():
        price_dct[idx] = bonds.loc[idx, "dirty_price"]

df = pd.DataFrame()
for file in m_list:
    etf_name = file.split(".")[0]
    temp = pd.read_csv(pcf_path + file, names = ["isin", "country", "coupon", "maturity", "quantity", "price", "accrued int", "original face"])
    temp = temp[temp.price.notnull()]
    temp["etf_name"] = etf_name
    temp = temp.set_index(["etf_name", "isin"])
    df = df.append(temp)
    





















