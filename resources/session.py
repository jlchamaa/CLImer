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
        self.inspection = 7
        self.sessionName = "JLC"
        self.solve = {}

    def processMainInput(self,inputKey):
        if(inputKey==' '):
            self.solve['time'] = self.timer()
            if(self.solve['time']>0):
                self.solve['plusTwo'] = True
                self.solve['session'] = self.sessionName 
                self.solve['date'] = datetime.datetime.now()
                self.dbObject.writeDb(self.solve)
            else:
                self.solve.clear()
                self.winMan.drawTime(0,True)
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
        while(True): #character for space
            now = time.time()
            tick = round(now-start-self.inspection,2)
            if(curtime!=tick):
                curtime=tick
                self.winMan.drawTime(abs(curtime),curtime>0)
            d = self.winMan.getCh()
            if d==32:
                if curtime<0:
                    start = now - self.inspection
                    continue
                else:
                    break
            elif d==27 and curtime<0:
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
        return scramble
    def play(self):
        status = True;
        while status: 
            self.solve.clear()
            scramble = self.createScramble()
            self.winMan.showScramble(scramble)
            self.solve['scramble'] = scramble
            self.winMan.showLog(self.dbObject.deliverDb(self.sessionName))
            mainInput = self.winMan.getKey() 
            status = self.processMainInput(mainInput)
