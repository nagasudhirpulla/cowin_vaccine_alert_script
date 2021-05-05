from appConfig import loadAppConfig
import datetime as dt
from getSessionsInDistrict import getSessionsInDistrict
from sendMail import sendMail
import time

appConf = loadAppConfig()
distId = appConf["districtId"]
tomDate = dt.datetime.now()+dt.timedelta(days=1)
host = appConf["host"]
port = appConf["port"]
mailUsername = appConf["mailUsername"]
mailPass = appConf["mailPass"]
fromMail = appConf["fromMail"]
toMail = appConf["toMail"]
msg = "Please check Cowin portal <a href=https://www.cowin.gov.in/home>https://www.cowin.gov.in/home</a> for vaccine booking for age less than 45 years"
sub = "Cowin portal Vaccine Availability alert"

mailSentAt = dt.datetime.now()-dt.timedelta(minutes=35)
def checkSessions():
    sessions = getSessionsInDistrict(distId, tomDate)
    if not len(sessions) == 0:
        capacities = [t["available_capacity"] for t in sessions if t["min_age_limit"]<45]
        if any([c>0 for c in capacities]):
            if dt.datetime.now() - mailSentAt > dt.timedelta(minutes=30):
                # dont send mail till half an hour
                sendMail(host, port, mailUsername, mailPass, msg, fromMail, toMail, sub)

while True:
    print("starting to check for vaccine sessions tomorrow")
    checkSessions()
    time.sleep(10)