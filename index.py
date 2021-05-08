from appConfig import loadAppConfig
import datetime as dt
from getSessionsInDistrict import getSessionsInDistrict
from sendMail import sendMail
import time

appConf = loadAppConfig()
distIds = appConf["districtIds"]

nowDate = dt.datetime.now()
numDays = appConf["numDays"]

host = appConf["host"]
port = appConf["port"]
mailUsername = appConf["mailUsername"]
mailPass = appConf["mailPass"]
fromMail = appConf["fromMail"]
toMails = appConf["toMails"]
mailIdleMinutes = appConf["mailIdleMinutes"]

datesList = [nowDate+dt.timedelta(days=k) for k in range(1, numDays+1)]
mailSentAt = dt.datetime.now()-dt.timedelta(minutes=35)


def checkSessions(reqDt):
    isMailSent = False
    for distId in distIds:
        distName = ""
        sessions = getSessionsInDistrict(distId, reqDt)
        if not len(sessions) == 0:
            capacityInfos = [t for t in sessions if (
                t["min_age_limit"] < 45) and (t["available_capacity"] > 0)]
            if len(capacityInfos) > 0:
                reqDtStr = dt.datetime.strftime(reqDt, "%d-%b-%Y")
                msg = "Please check Cowin portal <a href=https://www.cowin.gov.in/home>https://www.cowin.gov.in/home</a> for vaccine booking on {0} for age less than 45 years <br> ".format(
                    reqDtStr)
                try:
                    capacityStrs = ["Available capacity = {0}, {1}, {2}".format(
                        c["available_capacity"], c["name"], c["address"]) for c in capacityInfos]
                    distName = capacityInfos[0]["district_name"]
                except:
                    capacityStrs = [str(c) for c in capacityInfos]
                msg += '<br>'.join(capacityStrs)
                sub = "Cowin portal Vaccine Availability alert in {0}".format(
                    distName)
                sendMail(host, port, mailUsername, mailPass,
                         msg, fromMail, toMails, sub)
                isMailSent = True
    return isMailSent


while True:
    if dt.datetime.now() - mailSentAt > dt.timedelta(minutes=mailIdleMinutes):
        # dont check again till 15 mins after mail is sent
        isMailSent = False
        print("{0}: starting to check for vaccine slots for next {1} days".format(
            dt.datetime.now(), numDays))
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
