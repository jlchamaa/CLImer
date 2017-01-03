from resources import dbO
from resources import windowManager
import datetime
import time
import curses
import random


class session:
    def __init__(self,stdscr):
        self.dbObject = dbO.dbO()
        self.winMan = windowManager.windowManager(stdscr)
        self.inspection = 15
        self.session ='1' 
        self.solve = {}

    def processMainInput(self,inputKey):
        if(inputKey==' '):
            self.solve['time'] = self.timer()
            if(self.solve['time']>0):
                self.solve['plusTwo'] = True
                self.solve['session'] = self.session
                self.solve['date'] = datetime.datetime.now()
                self.dbObject.writeDb(self.solve)
            else:
                self.solve.clear()
                self.winMan.drawTime(0,True)
            return True
        elif(inputKey.isdigit()):
            self.session = str(inputKey)
            return True
        elif(inputKey == 'e'):
            return False
        else:
            return True

    def timer(self):
        self.winMan.noDelayOn(1)
        d="p" # not space
        curtime=0
        start = time.time()
        while(True): 
            now = time.time()
            tick = round(now-start-self.inspection,2)
            if(curtime!=tick): 
                curtime=tick
                self.winMan.drawTime(abs(curtime),curtime>0)
            d = self.winMan.getCh()
            if d==32: #number for space bar
                if curtime<0:
                    start = now - self.inspection
                    continue
                else:
                    break
            elif d==27 and curtime<0: #number for ESC, abort solve
                curses.beep()
                break
        self.winMan.noDelayOn(0)
        return curtime

    def createScramble(self):
        scramble = ""
        directions=["F","B","D","U","L","R"]
        lastDir="j"
        cases=[" ","' ","2 "]
        i=0
        while(i<20):
            i += 1
            newDir = directions[random.randint(0,5)]
            if(newDir==lastDir):
                i -= 1
                continue
            lastDir=newDir
            scramble += newDir
            scramble += cases[random.randint(0,2)]
            self.solve['scramble'] = scramble
            self.winMan.showScramble(scramble)

    def showSessionsAndLogs(self):
#return code (0,carry on) (1, restart loop) (2, abort)
            try:
                self.allSessions[self.session] #will raise exception if invalid
                self.winMan.showSessions(self.allSessions,self.session)
                self.winMan.showLog(self.dbObject.deliverDb(self.session))
                return 0
            except KeyError:
                newSeshName = self.winMan.ask('add')
                if newSeshName != None :
                    self.dbObject.addSession(self.session,newSeshName)
                    return 1
                elif self.session == '1':
                    return 2
                else:
                    self.session = '1'
                    return 1
    def play(self):
        status = True;
        while status: 
            self.allSessions = self.dbObject.getAllSessionNames()
            self.solve.clear()
            self.createScramble()
            value = self.showSessionsAndLogs()
            if value == 2:
                status = False
                continue
            elif value == 1:
                continue
                #value = 0 will just fall through, as we wish
            mainInput = self.winMan.getKey() 
            status = self.processMainInput(mainInput)
