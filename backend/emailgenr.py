from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
from email.mime.nonmultipart import MIMENonMultipart
import smtplib
from email import encoders
import pandas as pd

SERVER_SMTP_HOST = 'localhost'
SERVER_SMTP_PORT = 1025
SENDER_ADDRESS='projuserno1@gmail.com'
SENDER_PASSWORD='pguf dgyb eejd iwns'


def send_email(to_address,subject,message,content="text",attachment=None, fn=None):
    msg = MIMEMultipart()
    msg['To']=to_address
    msg['From']=SENDER_ADDRESS
    msg['Subject']=subject
    if content == "html":
        msg.attach(MIMEText(message,'html'))

        binary_pdf = open(attachment, 'rb')
        payload = MIMEBase('application', 'octate-stream', Name=attachment)
        payload.set_payload((binary_pdf).read())
        
        # enconding the binary into base64
        encoders.encode_base64(payload)
        
        # add header with pdf name
        payload.add_header('Content-Decomposition', 'attachment', filename=attachment)
        msg.attach(payload)
    else:
        msg.attach(MIMEText(message, 'plain'))
        attachment = MIMENonMultipart('text', 'csv', charset='utf-8')
        attachment.add_header('Content-Disposition', 'attachment', filename=fn)
        f = open(fn, "r")
        data = f.read()
        attachment.set_payload(data.encode('utf-8'))
        msg.attach(attachment)
    
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(SENDER_ADDRESS,SENDER_PASSWORD)
    text = msg.as_string()
    s.sendmail(SENDER_ADDRESS, to_address, text)
    s.quit()
    
    print("email sent***********************************")
    return True
