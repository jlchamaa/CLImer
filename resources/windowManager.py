import curses
from resources.digits import bigDigits,bigDigitsIndexes
class windowManager:

    def __init__(self,stdscr):
        curses.curs_set(0)
	self.windowArray = self.initializeWindows(stdscr)
	self.resizeWindows()

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

    def drawTime(self,time):
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
            self.windowArray[1].addstr(i,15,lineToWrite)
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
    def getKey(self):
        return self.windowArray[1].getkey() # wait for ch input from user

    def getCh(self):
        return self.windowArray[1].getch() # wait for ch input from user

    def noDelayOn(self,onSwitch):
        self.windowArray[1].nodelay(onSwitch)
