from resources import dbO
from resources import windowManager
import time
import curses
import random

class session:
    def __init__(self,stdscr):
        self.scramble = self.createScramble()
        self.dbObject = dbO.dbO()
        self.winMan = windowManager.windowManager(stdscr)


    def processMainInput(self,inputKey):
        if(inputKey==' '):
            self.timer()
            return True
        elif(inputKey == 'e'):
            return False
        else:
            self.winMan.refreshWindows()
            return True

    def timer(self):
        scramble = self.createScramble()
        self.winMan.noDelayOn(1)
        d="p" # not space
        curtime=0
        start = time.time()
        while(d!=32 and d!=27): #character for space
            now = time.time()
            tick = round(now-start,2) 
            if(curtime!=tick):
                curtime=tick
                self.winMan.drawTime(curtime)
            d = self.winMan.getCh()
        self.winMan.noDelayOn(0)
        #dbObject.writeDb(dbCursor,"main",curtime,0,"12-11-16",scramble)

    def createScramble(self):
        scramble = ""
        directions=["F","B","D","U","L","R"]
        lastDir=" "
        cases=[" ","\' ","2 "]
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
            mainInput = self.winMan.getKey() 
            status = self.processMainInput(mainInput)
