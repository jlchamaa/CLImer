import curses
from resources.digits import bigDigits,bigDigitsIndexes
class windowManager:

    def __init__(self,stdscr):
        curses.curs_set(0)
	self.initializeWindows(stdscr)
	self.resizeWindows()

    def initializeWindows(self,stdscr):
        self.mainScreen = stdscr
        self.winTimer = curses.newwin(1,1,0,0)
        self.winLog = curses.newwin(1,1,0,0)
        self.winOptions = curses.newwin(1,1,0,0)
        self.winScramble = curses.newwin(1,1,0,0)
        self.winStats = curses.newwin(1,1,0,0)

    def resizeWindows(self):
        (maxY,maxX) = self.mainScreen.getmaxyx()
        if(maxX>142):
            self.winTimer.resize(16,143)
            self.winTimer.mvwin(1,int((maxX-142)/2))
            self.winScramble.resize(3,maxX)
            self.winScramble.mvwin(17,0)
        else:
            horizontalDividerIndex = int(round(maxY*0.8))
            verticalDividerIndex = int(round(maxX*0.8))
            self.winTimer.resize(horizontalDividerIndex-1,verticalDividerIndex-1)
            self.winLog.mvwin(0,verticalDividerIndex+1)
            self.winLog.resize(horizontalDividerIndex-1,maxX-verticalDividerIndex+1)
            self.winOptions.mvwin(horizontalDividerIndex+1,0)
            self.winOptions.resize(maxY-horizontalDividerIndex+1,verticalDividerIndex-1)
            self.winStats.mvwin(horizontalDividerIndex+1,verticalDividerIndex+1)
            self.winStats.resize(maxY-horizontalDividerIndex+1,maxX-verticalDividerIndex+1)

    def showScramble(self,scramble):
        #self.winScramble.erase()
        (maxY,maxX)=self.winScramble.getmaxyx()
        startXCoord = (maxX-len(scramble))/2
        startYCoord = maxY-1
        self.winScramble.erase()
        self.winScramble.border()
        self.winScramble.addstr(1,startXCoord,scramble)
        self.winScramble.refresh()

    def drawTime(self,time,positive):
        tenmins   = int(time/600)
        minutes   = int(time/60) % 10
        seconds   = time%60
        tensPlace = int(seconds/10)
        onesPlace = int(seconds%10)
        jiffies   = seconds % 1
        tenths    = int(jiffies*10)
        hundredths= int(jiffies*100 % 10)
        i=0
        for digitsLine in bigDigits:
            lineToWrite = ""
            lineToWrite += self.fetchDigitChunk(digitsLine,tenmins,time>600) #tens place of mins
            lineToWrite += self.fetchDigitChunk(digitsLine,minutes,time>60) #singles of mins 
            lineToWrite += self.fetchDigitChunk(digitsLine,11,time>60) # add colon
            lineToWrite += self.fetchDigitChunk(digitsLine,tensPlace,time>10) # add tensPlace
            lineToWrite += self.fetchDigitChunk(digitsLine,onesPlace,True) # add onesPlace
            lineToWrite += self.fetchDigitChunk(digitsLine,10,True) # add decimal
            lineToWrite += self.fetchDigitChunk(digitsLine,tenths,True) # add tenths
            lineToWrite += self.fetchDigitChunk(digitsLine,hundredths,positive) # add hundredths
            self.winTimer.addstr(i,0,lineToWrite)
            i += 1
    def fetchDigitChunk(self,line,number,show):
        # 10 gets .   11 get : 
        if show:
            return  line[bigDigitsIndexes[number]:bigDigitsIndexes[number+1]]
        else:
            size = bigDigitsIndexes[number+1]-bigDigitsIndexes[number]
            space = ""
            for i in range(0,size):
                space += " "
            return space
    def getKey(self):
        return self.winTimer.getkey() # wait for ch input from user

    def getCh(self):
        return self.winTimer.getch() # wait for ch input from user

    def noDelayOn(self,onSwitch):
        self.winTimer.nodelay(onSwitch)
