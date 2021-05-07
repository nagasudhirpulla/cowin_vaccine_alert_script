import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def sendMail(host,port,uname,passwd,msg,from_mail,to_mail,subject):
    message = MIMEMultipart()
    message["Subject"] = subject
    server = smtplib.SMTP(host,port)
    server.starttls()
    server.login(uname,passwd)
    message.attach(MIMEText(msg,'html'))
    server.sendmail(from_mail, to_mail, message.as_string())
    server.quit()
    return