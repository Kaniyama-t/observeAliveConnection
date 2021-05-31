#!/usr/bin/env python3

import time
import requests
from datetime import datetime, timedelta, timezone
import pickle

JST = timezone(timedelta(hours=+9), 'JST')

HOME = "/home/kaniyama/.script/concnt/"
PATH_LOGS = HOME + "log/{0}".format(datetime.now().strftime("%Y-%m-%d.log"))

PATH_IS_DISCONNECTED = HOME + "var/isDisconnected"
PATH_LAST_DOWN_TIME  = HOME + "var/lastDownTime"
PATH_LAST_DOWN_TIME_INIT  = HOME + "var/lastDownInitTime"
PATH_RECENTLY_DOWN_TIME_LONG  = HOME + "var/recentlyDownLongTime"
PATH_RECENTLY_DOWN_SEC_LONG  = HOME + "var/recentlyDownLongSec"
PATH_I = HOME + "var/substringPointer"

I3BAR_COLOR_ESCAPE= "%{F-}"
I3BAR_COLOR_GREEN = "%{F#0f0}"
I3BAR_COLOR_RED   = "%{F#f00}"
I3BAR_FONT_MONO = '%{T6}'
I3BAR_FONT_END  = '%{T-}'

class concnt:

    def __init__(self):
        # Variable
        self.isDisconnected_ = False
        self.lastDownInitTime    = datetime(2001,1,1,0,0,0,0,tzinfo=JST)
        self.lastDownTime        = datetime(2001,1,1,0,0,0,0,tzinfo=JST)
        self.recentlyLongDownTime    = datetime(2001,1,1,0,0,0,0,tzinfo=JST)
        self.recentlyLongDownSec     = 0
        self.i = 0

    def loadAll(self):
        # Variable
        self.isDisconnected_ = pickle.load(open(PATH_IS_DISCONNECTED, "rb")) 
        self.lastDownInitTime = pickle.load(open(PATH_LAST_DOWN_TIME_INIT, "rb")) 
        self.lastDownTime = pickle.load(open(PATH_LAST_DOWN_TIME, "rb"))
        self.i = pickle.load(open(PATH_I, "rb"))
        self.recentlyLongDownTime    = pickle.load(open(PATH_RECENTLY_DOWN_TIME_LONG, "rb"))
        self.recentlyLongDownSec     = pickle.load(open(PATH_RECENTLY_DOWN_SEC_LONG, "rb"))
        return self

    def dumpAll(self):
        pickle.dump(self.isDisconnected_,open(PATH_IS_DISCONNECTED, "wb")) 
        pickle.dump(self.lastDownInitTime,open(PATH_LAST_DOWN_TIME_INIT, "wb")) 
        pickle.dump(self.lastDownTime,open(PATH_LAST_DOWN_TIME, "wb"))
        pickle.dump(self.i, open(PATH_I, "wb"))
        pickle.dump(self.recentlyLongDownTime,open(PATH_RECENTLY_DOWN_TIME_LONG, "wb"))
        pickle.dump(self.recentlyLongDownSec, open(PATH_RECENTLY_DOWN_SEC_LONG, "wb"))
        return self

    def tryConnection(self):
        try:
            r = requests.get('http://ok.kaniyama.net/',timeout=(1,1))
            if(r.status_code >= 400):
                self.onDisconnect()
            else:
                self.onConnect()
        except:
            self.onDisconnect()
        finally:
            lastDownSec = (self.lastDownTime - self.lastDownInitTime).seconds
            lastDownTimeStr = self.lastDownTime.strftime("%H:%M")
            msg = "{0}({1:>2}sec)".format(lastDownTimeStr, lastDownSec)
            self.printForI3Bar(msg)
        return self

    def onConnect(self):
        if self.isDisconnected_:
            self.onReconnected()
        self.isDisconnected_ = False

    def onReconnected(self):
        lastDownSec = (self.lastDownTime - self.lastDownInitTime).seconds
        self.lastDownTime = datetime.now(tz=JST)

        if (lastDownSec > 15):
            self.recentlyLongDownTime = datetime.now(tz=JST)
            self.recentlyLongDownSec  = lastDownSec

        with open(PATH_LOGS,'at') as fd:
            fd.write("{0},{1},{2}\n".format(
                self.lastDownInitTime.isoformat(),
                lastDownSec,
                self.lastDownTime.isoformat())
            )
            fd.close()

    def onDisconnect(self):
        if not self.isDisconnected_: 
            self.onResumeDisconnecting()
        self.lastDownTime = datetime.now(tz=JST)
    
    def onResumeDisconnecting(self):
        self.lastDownInitTime = datetime.now(tz=JST)
        self.isDisconnected_ = True
        self.i = 0

    def recentTimeText(self,msg):
        recentlyDownTimeStr = self.recentlyLongDownTime.strftime("%H:%M")
        recentlyLongDownMsg = "{0}({1}sec)".format(recentlyDownTimeStr,self.recentlyLongDownSec)
        self.i += 1
        if(self.i >= 5): self.i = 1
        if (self.i <= 2):
            return msg
        else:
            return recentlyLongDownMsg

    def scrollingText(self,msg):
        msgl = len(msg)
        ret = msg[self.i:((self.i+10) if (self.i+10) <= msgl else msgl)]
        ret += ' ' * (0 if (self.i+10) <= msgl else (10 - (msgl - self.i)))
        self.i += 1
        if(self.i >= len(msg)):
            self.i = 0
        return ret
    
    def printForI3Bar(self, msg):
        print("{0}●{1} {2}{3}{4}".format(
            I3BAR_COLOR_RED if self.isDisconnected_ else I3BAR_COLOR_GREEN,
            I3BAR_COLOR_ESCAPE,
            I3BAR_FONT_MONO,
            msg, # scrollingText(msg),
            I3BAR_FONT_END)
        )

    def loggingDisconnect():
        pass


# loadAll()
concnt().loadAll().tryConnection().dumpAll()
