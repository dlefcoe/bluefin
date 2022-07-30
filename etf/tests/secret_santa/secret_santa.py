# https://gradientdescending.com/secret-santa-list-using-python/

# SECRET SANTA

# LIBRARIES
import numpy as np
import datetime
import pandas as pd
import smtplib
import app_wrd
import os

# DATE AND TIME
dt = datetime.datetime.now()
date = dt.strftime('%Y-%m-%d at %I:%M%p')
datem = dt.strftime('%Y-%m-%d')

# EMAIL DICTIONARY
# replace the names and emails with those participating
csv_file_path = os.path.dirname(os.path.abspath(__file__))
csv_file_name = os.path.join(csv_file_path, 'email_list.csv')
fam = pd.read_csv(csv_file_name, squeeze=True, index_col=0).to_dict()

# fam = {
# 'charles'   : 'dlefcoe@bluefintrading.com',
# 'Bob'     : 'dlefcoe@bluefintrading.com',
# 'Chris'   : 'dlefcoe@bluefintrading.com',
# 'Fred'    : 'dlefcoe@bluefintrading.com'
# }

# SELECT SECRET SANTAS
santa = list(np.random.choice(list(fam.keys()), len(list(fam.keys())), replace = False))
recvr = []
for k in range(-1, len(santa)-1):
	recvr.append(santa[k])
			
# STARTING EMAILS
smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.ehlo()
smtpObj.starttls()
eml = 'dlefcoe@bluefintrading.com'
pwd = app_wrd.w
smtpObj.login(eml, pwd)

# SENDING EMAILS
for k in range(len(fam)):
	smtpObj.sendmail(eml, fam[santa[k]], \
	'Subject: Bluefin Secret Santa \
	\nHo Ho Ho %s! \
	\n\nChristmas at Bluefin is almost here, \
	\nTime to find that Christmas cheer! \
	\n\nThis year you are buying for....... %s! \
	\n\nThis was sent on %s.' % (santa[k], recvr[k], date))

# QUIT SERVER
smtpObj.quit()

# STORE SELECTIONS FOR SAFE KEEPING
santadf = pd.DataFrame({'santa':santa, 'recvr':recvr})
results_csv = csv_file_name = os.path.join(csv_file_path, 'Secret Santa list ' + datem + '.csv')
santadf.to_csv(results_csv)

