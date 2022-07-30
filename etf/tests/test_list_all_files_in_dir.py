
import os

inspect_path = 'Y:\\Benjamin\\Market_Making\\PCFs\\iShares_US\\20211221'
files_in_folder = [f for f in os.listdir(inspect_path) if os.path.isfile(os.path.join(inspect_path, f))]

print(f'there are {len(files_in_folder)} files in the folder.')
print('here are the files:\r',files_in_folder)


print()
print('the base dir list:')
base_dir = 'Y:\\Benjamin\\Market_Making\\PCFs'
issuer_dir_list = ['AMUNDI_Bonds', 'BNP_Bonds', 'DBX2_Bonds' ]
folder_date = '20211222'
for i in issuer_dir_list:
    print()
    print(f'pcf files for {i}:')
    a = os.listdir(base_dir + '\\' + i + '\\' + folder_date)
    print('files found:', len(a))
    print(a)

    

