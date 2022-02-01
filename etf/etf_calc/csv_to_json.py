'''

price PFC from first principals

'''

import datetime as dt
from os import error
import pandas as pd
import csv
import json


# current date
current_date = dt.datetime.today().strftime('%Y%m%d')


# get pcf
pcf_folder_base = 'Y:\\Benjamin\\Market_Making\\PCFs\\UBS_Bonds\\'
pcf_folder_base = pcf_folder_base + current_date + "\\"
pcf_file_name = "CBUS5E_" + current_date + ".csv"
pcf_full_path = pcf_folder_base + pcf_file_name

print('opening file:')
print(pcf_full_path)

# try:
#     df = pd.read_csv(pcf_full_path,  skiprows=20, header=21, nrows=175)
#     print('data read')
# except error:
#     print('error reading file')
#     quit()
    
# print(df)


# open and read the csv
data = {}
with open(pcf_full_path) as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for rows in csv_reader:
        key = rows['id']
        data[key] = rows

print(data)



