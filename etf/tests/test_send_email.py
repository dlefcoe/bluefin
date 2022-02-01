'''


code to send a simple email

app password generated from google:
    account >> security >> app passwords


'''


import smtplib

from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

app_password = 'qqhllrqziubtacoj'


def main():
        
       sendEmail()



def sendEmail():
    
    try:    
        msg = MIMEMultipart()
        msg['Subject'] = 'test email'
        msg['From'] = 'dlefcoe@bluefintrading.com'
        msg['To'] = 'dlefcoe@bluefintrading.com'
            
        # That is what u see if dont have an email reader:
        msg.preamble = 'Multipart message.\n'
            
        # This is the textual part:
        part = MIMEText('this is a test email from DL trading')
        msg.attach(part)

        # Create an instance in SMTP server
        server = smtplib.SMTP('smtp.gmail.com')
        server.connect('smtp.gmail.com',587) 
        server.ehlo()
        server.starttls()
        server.login('dlefcoe@bluefintrading.com', app_password)
            
        # Send the email
        server.sendmail(msg['From'], msg['To'],msg.as_string())
    except Exception as ex:
        print (ex)


                        
if __name__ == '__main__':
        
        main()


