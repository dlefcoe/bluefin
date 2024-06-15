


import datetime as dt
import csv


class Etf:
    ''' get pcf for a given issuer and given date
    
    parameters:

        issuer (str): the issuer name
        ticker (str): the ticker of the ETF
        pcf_date (str): the date of the ETF pcf file in yyyymmdd format
    
    '''

    def __init__(self, issuer:str, ticker:str, pcf_date:str) -> None:
        self.issuer = issuer
        self.ticker = ticker
        self.pcf_date = pcf_date
        self.generate_file_path()
        self.get_pcf_file()

    def generate_file_path(self):
        ''' function to generate a file path '''

        # generate date strings for making file path names
        date_yyyymmdd = dt.datetime.today().strftime('%Y%m%d')
        date_ddmmyy = dt.datetime.today().strftime('%d%m%y')
        yesterday = dt.datetime.now() - dt.timedelta(1)
        prev_date_ddmmyy = yesterday.strftime('%d%m%y')

        if self.issuer == 'ishares':
            folder_path = 'Y:\\Benjamin\\Market_Making\\PCFs\\ISHARES_Bonds\\' + date_yyyymmdd + '\\'
            file_name = 'CPCF' + self.ticker + prev_date_ddmmyy + 'A'
            file_extension = '.csv'

            self.full_path_and_name = folder_path + file_name + file_extension
        else:
            self.full_path_and_name = None

    
    def get_pcf_file(self):
        ''' get pcf file '''

        # check if folder exists
        # assume that folder exists for now

        # read file with csv first to determine first and last row
        if self.issuer == 'ishares':
            # for ishares look at columns 6 & 7 to identify first and last row
            with open(self.full_path_and_name, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                i = 0
                for row in spamreader:
                    if len(row) > 12:
                        print(row)
                        break
                    i = i + 1
                    if i > 100:
                        break


            pass
        else:
            pass
    

        return 100


    def __repr__(self):
        return f'''Etf class values
            issuer: {self.issuer},
            path name: {self.full_path_and_name},
            date: {self.pcf_date}'''
        

def main():
    # create etf instance
    e = Etf('ishares', 'ieac', '20211112')
    print(e)


# main guard idiom
if __name__=='__main__':
    main()



