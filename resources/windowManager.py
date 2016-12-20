import curses
from resources.digits import bigDigits,bigDigitsIndexes
NumericWidth = 142
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
        if(maxX>NumericWidth):
            self.winTimer.resize(16,NumericWidth+1)
            self.winTimer.mvwin(1,int((maxX-NumericWidth)/2))
            self.winScramble.resize(3,maxX)
            self.winScramble.mvwin(17,0)
            self.winLog.resize(20,60)
            self.winLog.mvwin(22,2)
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

    def showLog(self,dataObj):
        self.winLog.clear()
        self.winLog.border()
        line = 0
        for i in dataObj:
            stringToWrite = str(i[0])
            self.winLog.addstr(line,1,stringToWrite.rjust(17))
            line +=1
        self.winLog.refresh()

    def drawTime(self,time,positive):
        digits = self.secondsToDigits(time)
        i=0
        for digitsLine in bigDigits:
            lineToWrite = ""
            lineToWrite += self.fetchDigitChunk(digitsLine,digits['tenmins'],time>600) #tens place of mins
            lineToWrite += self.fetchDigitChunk(digitsLine,digits['minutes'],time>60) #singles of mins 
            lineToWrite += self.fetchDigitChunk(digitsLine,11,time>60) # add colon
            lineToWrite += self.fetchDigitChunk(digitsLine,digits['tensPlace'],time>10) # add tensPlace
            lineToWrite += self.fetchDigitChunk(digitsLine,digits['onesPlace'],True) # add onesPlace
            lineToWrite += self.fetchDigitChunk(digitsLine,10,True) # add decimal
            lineToWrite += self.fetchDigitChunk(digitsLine,digits['tenths'],True) # add tenths
            lineToWrite += self.fetchDigitChunk(digitsLine,digits['hundredths'],positive) # add hundredths
            indentation = (NumericWidth - len(lineToWrite))/2
            self.winTimer.addstr(i,indentation,lineToWrite)
            i += 1
    def secondsToDigits(self,time):
        timeDigits = {}
        timeDigits['tenmins'] = int(time/600)
        timeDigits['minutes'] = int(time/60) % 10
        seconds = time%60
        timeDigits['tensPlace'] = int(seconds/10)
        timeDigits['onesPlace'] = int(seconds%10)
        jiffies = seconds % 1
        timeDigits['tenths'] = int(jiffies*10)
        timeDigits['hundredths'] = int(jiffies*100 % 10)
        return timeDigits
 
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
