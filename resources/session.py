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
        self.penalty = 2
        self.session ='1' 
        self.solve = {}

    def processMainInput(self,inputKey):
        if(inputKey==' '):
            self.winMan.centerTime()
            result,p2 = self.timer()
            self.winMan.resizeWindows()
            if result is None or result>0:
                self.solve['time'] = result
                self.solve['plusTwo'] = p2
                self.solve['session'] = self.session
                self.solve['date'] = datetime.datetime.now()
                self.dbObject.writeDb(self.solve)
            self.solve.clear()
            self.createScramble()
            return 2
        elif(inputKey.isdigit()):
            self.session = str(inputKey)
            return 2
        elif(inputKey == 'q'):
            return 0
        elif(inputKey == 'r'):
            self.dbObject.removeRecord(self.session)
            return 2
        elif(inputKey == 'd'):
            self.dbObject.DNF(self.session)
            return 2
        elif(inputKey == 'p'):
            self.dbObject.plusTwo(self.session)
            return 2
        elif(inputKey == 'e'):
            if self.winMan.ask('removeSession',self.session):
                self.dbObject.deleteSession(self.session)
                self.session = '1'
            return 2
        else:
            return 1

    def timer(self):
        self.winMan.noDelayOn(1)
        p2 = False
        d="p" # not space
        curtime=0
        start = time.time()
        while d is not 32: 
            if d == 27:
                self.winMan.noDelayOn(0)
                return -1,False
            now = time.time()
            tick = round(now-start-self.inspection-self.penalty,2)
            if(curtime!=tick): 
                curtime=tick
                timeToDraw = curtime+self.penalty if curtime < -1 * self.penalty else 2
                self.winMan.drawTime(abs(timeToDraw),False)
                if curtime >= -1 * self.penalty and curtime < 0:
                    p2 = True
                elif curtime >= 0 :
                    self.winMan.noDelayOn(0)
                    return None,False
            d = self.winMan.getCh()
        start = time.time()
        d = 'p'
        while d is not 32:               
            now = time.time()
            tick = round(now-start,2)
            if(curtime!=tick): 
                curtime=tick
                self.winMan.drawTime(abs(curtime),True)
            d = self.winMan.getCh()
        self.winMan.noDelayOn(0)
        if p2:
            curtime += self.penalty
        return curtime,p2

    def createScramble(self):
        scramble = ""
        directions=["F","U","R","B","D","L"]
        lastDir= -1
        cases=[" ","' ","2 "]
        i=0
        while(i<25):
            i += 1
            if lastDir >= 0:
                while lastDir % 3 == newDir % 3 : newDir = random.randint(0,5)
            else:
                newDir = random.randint(0,5)
            lastDir=newDir
            scramble += directions[newDir]
            scramble += cases[random.randint(0,2)]
        self.solve['scramble'] = scramble
        self.winMan.showScramble(scramble)

    def showSessionsAndLogs(self):
#return code (0,carry on) (1, restart loop) (2, abort)
            try:
                self.allSessions[self.session] #will raise exception if invalid
                self.winMan.showSessions(self.allSessions,self.session)
                self.winMan.showLog(self.dbObject.deliverDb(self.session,30))
                return 0
            except KeyError:
                newSeshName = self.winMan.ask('add',None)
                if newSeshName != None :
                    self.dbObject.addSession(self.session,newSeshName)
                    return 1
                elif self.session == '1':
                    return 2
                else:
                    self.session = '1'
                    return 1
    def play(self):
        status = 2;
        self.createScramble()
        while status == 2: 
            self.allSessions = self.dbObject.getAllSessionNames()
            value = self.showSessionsAndLogs()
            if value == 2:
                status = 0
                continue
            elif value == 1:
                continue
            #value = 0 will just fall through, as we wish
            
            status = 1
            while status == 1:
                mainInput = self.winMan.getKey() 
                status = self.processMainInput(mainInput)
