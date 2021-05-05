from appConfig import loadAppConfig
import datetime as dt
from getSessionsInDistrict import getSessionsInDistrict
from sendMail import sendMail
import time

appConf = loadAppConfig()
distId = appConf["districtId"]

nowDate = dt.datetime.now()
numDays = 3
datesList = [nowDate+dt.timedelta(days=k) for k in range(numDays+1)]

host = appConf["host"]
port = appConf["port"]
mailUsername = appConf["mailUsername"]
mailPass = appConf["mailPass"]
fromMail = appConf["fromMail"]
toMail = appConf["toMail"]
sub = "Cowin portal Vaccine Availability alert"

mailSentAt = dt.datetime.now()-dt.timedelta(minutes=35)
def checkSessions(reqDt):
    isMailSent = False
    sessions = getSessionsInDistrict(distId, reqDt)
    if not len(sessions) == 0:
        capacities = [t["available_capacity"] for t in sessions if t["min_age_limit"]<45]
        if any([c>0 for c in capacities]):
            reqDtStr = dt.datetime.strftime(reqDt, "%d-%b-%Y")
            msg = "Please check Cowin portal <a href=https://www.cowin.gov.in/home>https://www.cowin.gov.in/home</a> for vaccine booking on {0} for age less than 45 years".format(reqDtStr)
            if dt.datetime.now() - mailSentAt > dt.timedelta(minutes=30):
                # dont send mail till half an hour
                sendMail(host, port, mailUsername, mailPass, msg, fromMail, toMail, sub)
                isMailSent = True
    return isMailSent

while True:
    print("{0}: starting to check for vaccine sessions for next {1} days".format(dt.datetime.now(), numDays))
    isMailSent = False
    try:
        for d in datesList:
            mailSentResult = checkSessions(d)
            if mailSentResult == True:
                isMailSent = True
        if isMailSent:
            mailSentAt = dt.datetime.now()
    except:
        print("error occurred")
    time.sleep(10)