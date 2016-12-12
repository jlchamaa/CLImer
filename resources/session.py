from resources.digits import bigDigits,bigDigitsIndexes
from resources import dbO
import time
import curses
import random

class session:
    def __init__(self):
       self.scramble="" 
    def initializeWindows(self,stdscr):
        windowArray= []
        windowArray.append(stdscr)
        for i in range(1,5): #inconsequential iterator
            windowArray.append(curses.newwin(1,1,0,0))
        return windowArray

#   stdscr = 0
#  ############
#  # 1    # 2 #
#  #      #   #
#  ############
#  #  3   # 4 #
#  ############

    def resizeWindows(self):
        (maxY,maxX) = self.windowArray[0].getmaxyx()
        horizontalDividerIndex = int(round(maxY*0.8))
        verticalDividerIndex = int(round(maxX*0.8))
        self.windowArray[1].resize(horizontalDividerIndex-1,verticalDividerIndex-1)
        self.windowArray[2].mvwin(0,verticalDividerIndex+1)
        self.windowArray[2].resize(horizontalDividerIndex-1,maxX-verticalDividerIndex+1)
        self.windowArray[3].mvwin(horizontalDividerIndex+1,0)
        self.windowArray[3].resize(maxY-horizontalDividerIndex+1,verticalDividerIndex-1)
        self.windowArray[4].mvwin(horizontalDividerIndex+1,verticalDividerIndex+1)
        self.windowArray[4].resize(maxY-horizontalDividerIndex+1,maxX-verticalDividerIndex+1)

    def refreshWindows(self):
        for i in range(1,5):
            self.windowArray[i].border()
            self.windowArray[i].refresh()

    def processMainInput(self,inputKey):
        if(inputKey==' '):
            self.timer(self.windowArray[0])
            return True
        elif(inputKey == 'e'):
            return False
        else:
            self.refreshWindows()
            return True

    def timer(self,window):
        scramble = self.createScramble()
        window.addstr(30,2,scramble)
        window.nodelay(1)
        d="p" # not space
        curtime=0
        start = time.time()
        while(d!=32 and d!=27): #character for space
            now = time.time()
            tick = round(now-start,2) 
            if(curtime!=tick):
                curtime=tick
                self.drawTime(curtime,window)
            d=window.getch()
        window.nodelay(0)
        #dbObject.writeDb(dbCursor,"main",curtime,0,"12-11-16",scramble)
    def drawTime(self,time,window):
        tenmins   = int(time/600)
        minutes   = int(time/60) % 10
        seconds   = time%60
        tensPlace = int(seconds/10)
        onesPlace = int(seconds%10)
        jiffies   = seconds % 1
        tenths    = int(jiffies*10)
        hundredths= int(jiffies*100 % 10)
        i=10
        for digitsLine in bigDigits:
            lineToWrite = ""
            lineToWrite += self.fetchDigitChunk(digitsLine,tenmins,time<600) #tens place of mins
            lineToWrite += self.fetchDigitChunk(digitsLine,minutes,time<60) #singles of mins 
            lineToWrite += self.fetchDigitChunk(digitsLine,11,time<60) # add colon
            lineToWrite += self.fetchDigitChunk(digitsLine,tensPlace,time<10) # add tensPlace
            lineToWrite += self.fetchDigitChunk(digitsLine,onesPlace,time<1) # add tensPlace
            lineToWrite += self.fetchDigitChunk(digitsLine,10,False) # add tensPlace
            lineToWrite += self.fetchDigitChunk(digitsLine,tenths,False) # add tensPlace
            lineToWrite += self.fetchDigitChunk(digitsLine,hundredths,False) # add tensPlace
            window.addstr(i,15,lineToWrite)
            i += 1
    def fetchDigitChunk(self,line,number,empty):
# 10 gets .   11 get : 
        if empty:
            size = bigDigitsIndexes[number+1]-bigDigitsIndexes[number]
            space = ""
            for i in range(0,size):
                space += " "
            return space
        else:
            return  line[bigDigitsIndexes[number]:bigDigitsIndexes[number+1]]

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

    def play(self,stdscr):
        dbObject = dbO.dbO()
        curses.curs_set(0)
        self.windowArray = self.initializeWindows(stdscr)
        self.resizeWindows()
        self.refreshWindows()
        status = True;
        while status: 
            mainInput = self.windowArray[1].getkey() # wait for ch input from user
            status = self.processMainInput(mainInput)