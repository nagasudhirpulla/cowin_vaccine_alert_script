from appConfig import loadAppConfig
import datetime as dt
from getSessionsInDistrict import getSessionsInDistrict
from sendMail import sendMail
import time

appConf = loadAppConfig()
distId = appConf["districtId"]

nowDate = dt.datetime.now()
numDays = 1
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
        capacityInfos = [t for t in sessions if t["min_age_limit"]<45]
        if any([c["available_capacity"]>0 for c in capacityInfos]):
            reqDtStr = dt.datetime.strftime(reqDt, "%d-%b-%Y")
            msg = "Please check Cowin portal <a href=https://www.cowin.gov.in/home>https://www.cowin.gov.in/home</a> for vaccine booking on {0} for age less than 45 years <br> ".format(reqDtStr)
            capacityStrs = ["Available capacity = {0}, {1}, {2}".format(c["available_capacity"], c["name"], c["address"]) for c in capacityInfos]
            msg += '<br>'.join(capacityStrs) 
            sendMail(host, port, mailUsername, mailPass, msg, fromMail, toMail, sub)
            isMailSent = True
    return isMailSent

while True:
    if dt.datetime.now() - mailSentAt > dt.timedelta(minutes=15):
        # dont check again till 15 mins after mail is sent
        isMailSent = False
        print("{0}: starting to check for vaccine slots for next {1} days".format(dt.datetime.now(), numDays))
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