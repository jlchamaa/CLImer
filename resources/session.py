from resources import dbO
from resources import windowManager
import time
import curses
import random

class session:
    def __init__(self,stdscr):
        self.dbObject = dbO.dbO()
        self.winMan = windowManager.windowManager(stdscr)
        self.inspection = 15


    def processMainInput(self,inputKey):
        if(inputKey==' '):
            self.timer()
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
        while(d!=32 and d!=27): #character for space
            now = time.time()
            tick = round(now-start-self.inspection,2)
            if(curtime!=tick):
                curtime=tick
                self.winMan.drawTime(abs(curtime),curtime>0)
            d = self.winMan.getCh()
        self.winMan.noDelayOn(0)

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
            scramble = self.createScramble()
            self.winMan.showScramble(scramble)
            mainInput = self.winMan.getKey() 
            status = self.processMainInput(mainInput)
