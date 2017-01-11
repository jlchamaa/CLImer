import curses
from resources.digits import bigDigits,bigDigitsIndexes
NumericWidth = 142
class windowManager:
    def __init__(self,stdscr):
        curses.curs_set(0)
        self.initializeColors()
        self.initializeWindows(stdscr)
        self.resizeWindows()
        self.blinking = False;
    def initializeColors(self):
        if curses.can_change_color():
            curses.init_color(1,100,100,100) #color 1 is grey
            curses.init_pair(1,curses.COLOR_CYAN,1) #timer
            curses.init_pair(2,curses.COLOR_WHITE,1) # background
            curses.init_pair(3,1,curses.COLOR_CYAN) # scramble

        else:
            curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_BLACK)
            curses.init_pair(2,curses.COLOR_WHITE,curses.COLOR_BLACK)
    def initializeWindows(self,stdscr):
        self.mainScreen = stdscr
        self.winTimer = curses.newwin(1,1,0,0)
        self.winLog = curses.newwin(1,1,0,0)
        self.winOptions = curses.newwin(1,1,0,0)
        self.winScramble = curses.newwin(1,1,0,0)
        self.winStats = curses.newwin(1,1,0,0)

    def resizeWindows(self):
        (maxY,maxX) = self.mainScreen.getmaxyx()
        self.mainScreen.bkgd(' ',curses.color_pair(1))
        self.mainScreen.refresh()
        if(maxX>NumericWidth):
            self.winTimer.mvwin(1,int((maxX-NumericWidth)/2))
            self.winTimer.resize(16,NumericWidth+1)
            self.winTimer.bkgd(' ',curses.color_pair(1))
            self.winScramble.mvwin(17,0)
            self.winScramble.resize(3,maxX)
            self.winScramble.bkgd(' ',curses.color_pair(1))
            self.winOptions.mvwin(21,0)
            self.winOptions.resize(7,maxX)
            self.winOptions.bkgd(' ',curses.color_pair(1))
            self.winLog.mvwin(30,2)
            self.winLog.resize(30,60)
            self.winLog.bkgd(' ',curses.color_pair(1))
        else:
            raise ValueError('toosmall')
        curses.doupdate()

    def centerTime(self):
        (maxY,maxX) = self.mainScreen.getmaxyx()
        self.winTimer.mvwin(int((maxY-16)/2),int((maxX-NumericWidth)/2))
        self.mainScreen.bkgd(' ',curses.color_pair(1))
        self.mainScreen.refresh()

    def showScramble(self,scramble):
        #self.winScramble.erase()
        (maxY,maxX)=self.winScramble.getmaxyx()
        startXCoord = int((maxX-len(scramble))/2)
        startYCoord = maxY-1
        self.winScramble.erase()
        self.winScramble.border()
        self.winScramble.addstr(1,startXCoord,scramble)
        self.winScramble.refresh()

    def showLog(self,dataObj):
        self.winLog.clear()
        self.winLog.border()
        line = 1
        for i in dataObj:
            stringToWrite = str(i[1])+ ". " 
            time=i[0]
            if time == None:
                stringToWrite += "     DNF"
            else:
                mins = int(time / 60)
                sex = time % 60
                timeToWrite=""
                if mins > 0:
                    timeToWrite += str(mins) + ":"
                    timeToWrite += "{:0>5.2f}".format(sex)
                else:
                    timeToWrite += "{0:.2f}".format(sex)
                stringToWrite += timeToWrite.rjust(8)
                if i[2]:
                    stringToWrite+="+"
            self.winLog.addstr(line,2,stringToWrite)
            line +=1
        self.winLog.refresh()

    def showSessions(self,names,current):
        self.winOptions.clear()
        self.winOptions.border()
        self.winOptions.addstr(4,1,"(Q)uit , (P)lus 2 , (D)NF , (E)rase Session , (R)emove Time, (space) Start")
        column = 10
        for curNum,curName in sorted(names.items()):
            attributes = curses.A_NORMAL
            if curNum == str(current):
                attributes = curses.A_REVERSE
            strToWrite = '{:^30}'.format(curNum +'. ' + curName)
            self.winOptions.addstr(2,column,strToWrite,attributes)
            column += len(strToWrite)
        self.winOptions.refresh()

    def ask(self,question,context):
        if question == 'add':
            strToWrite = "Do you want to create a new session? (y/n): "
            self.winOptions.clear()
            self.winOptions.border()
            self.winOptions.addstr(2,7,strToWrite)
            self.winOptions.refresh()
            response = self.winOptions.getkey()
            if response.lower() == 'y':
                curses.echo()
                curses.curs_set(1)
                self.winOptions.addstr(" Name: ")
                seshName = self.winOptions.getstr()
                curses.curs_set(0)
                curses.noecho()
                return seshName
            else:
                return None 
        if question == 'removeSession':
            strToWrite = "Do you want to delete this session and all of its times? (y/n): "
            self.winOptions.clear()
            self.winOptions.border()
            self.winOptions.addstr(2,7,strToWrite)
            self.winOptions.refresh()
            response = self.winOptions.getkey()
            if response.lower() == 'y':
                return True
            else:
                return False

    def drawTime(self,time,positive):
        if not positive:
            if int(time) == 3 or int(time) == 2 or int(time) == 4: 
                if not self.blinking:
                    if (int(time*10) % 10) == 1:
                        self.mainScreen.bkgd(' ',curses.color_pair(3))
                        self.mainScreen.refresh()
                        self.blinking = not self.blinking
                if self.blinking:
                    if (int(time*10) % 10) == 0:
                        self.mainScreen.bkgd(' ',curses.color_pair(1))
                        self.mainScreen.refresh()
                        self.blinking = not self.blinking
            if int(time) == 1 or int(time) == 0: 
                if not self.blinking:
                    if (int(time*10) % 4) == 2:
                        self.mainScreen.bkgd(' ',curses.color_pair(3))
                        self.mainScreen.refresh()
                        self.blinking = not self.blinking
                if self.blinking:
                    if (int(time*10) % 4) == 0:
                        self.mainScreen.bkgd(' ',curses.color_pair(1))
                        self.mainScreen.refresh()
                        self.blinking = not self.blinking
        if positive and self.blinking:
            self.mainScreen.bkgd(' ',curses.color_pair(1))
            self.mainScreen.refresh()
            self.blinking = not self.blinking
            

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
            indentation = (NumericWidth - len(lineToWrite))//2
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
