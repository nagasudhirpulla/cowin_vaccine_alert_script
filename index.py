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
msg = "Please check Cowin portal https://www.cowin.gov.in/home for vaccine booking for age less than 45 years"
sub = "Cowin portal Vaccine Availability alert"

def checkSessions():
    sessions = getSessionsInDistrict(distId, tomDate)
    if not len(sessions) == 0:
        capacities = [t["available_capacity"] for t in sessions if t["min_age_limit"]<45]
        if any([c>0 for c in capacities]):
            sendMail(host, port, mailUsername, mailPass, msg, fromMail, toMail, sub)

while True:
    checkSessions()
    time.sleep(10)