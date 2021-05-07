from sendMail import sendMail
from appConfig import loadAppConfig

appConf = loadAppConfig()
host = appConf["host"]
port = appConf["port"]
mailUsername = appConf["mailUsername"]
mailPass = appConf["mailPass"]
fromMail = appConf["fromMail"]
toMail = appConf["toMail"]
msg = "Please check Cowin portal <a href=https://www.cowin.gov.in/home>https://www.cowin.gov.in/home</a> for vaccine booking for age less than 45 years"
sub = "Cowin portal Vaccine Availability alert"

sendMail(host, port, mailUsername, mailPass, msg, fromMail, [fromMail], sub)