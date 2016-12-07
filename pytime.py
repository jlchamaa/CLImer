from digits import bigDigits,bigDigitsIndexes
import time
import curses

def initializeWindows(stdscr):
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

def resizeWindows(windowArray):
    (maxY,maxX) = windowArray[0].getmaxyx()
    horizontalDividerIndex = int(round(maxY*0.8))
    verticalDividerIndex = int(round(maxX*0.8))
    windowArray[1].resize(horizontalDividerIndex-1,verticalDividerIndex-1)
    windowArray[2].mvwin(0,verticalDividerIndex+1)
    windowArray[2].resize(horizontalDividerIndex-1,maxX-verticalDividerIndex+1)
    windowArray[3].mvwin(horizontalDividerIndex+1,0)
    windowArray[3].resize(maxY-horizontalDividerIndex+1,verticalDividerIndex-1)
    windowArray[4].mvwin(horizontalDividerIndex+1,verticalDividerIndex+1)
    windowArray[4].resize(maxY-horizontalDividerIndex+1,maxX-verticalDividerIndex+1)

def refreshWindows(windowArray):
    for i in range(1,5):
        windowArray[i].border()
        windowArray[i].refresh()

def processMainInput(inputKey,windowArray):
    if(inputKey==' '):
        windowArray[1].nodelay(1)
        timer(windowArray[1])
        windowArray[1].nodelay(0)
    else:
        windowArray[3].addstr(4,4,bigDigits[3])
        refreshWindows(windowArray)

def timer(window):
    d="p" # not space
    curtime=0
    start = time.time()
    while(d!=32 and d!=27): #character for space
        now = time.time()
        tick = round(now-start,1) 
        if(curtime!=tick):
            curtime=tick
            window.addstr(17,0, str(curtime))
            drawTime(curtime,window,False)
        d=window.getch()
    #TODO add database logic

def drawTime(time,window,showJiffies):
    window.clear()
    minutes   = int(time/60)
    seconds   = time%60
    tensPlace = int(seconds/10)
    onesPlace = int(seconds%10)
    jiffies   = seconds % 1
    tenths    = int(jiffies*10)
    hundredths= int(jiffies*100)
    i=1
    for digitsLine in bigDigits:
        lineToWrite = ""
        if(minutes>0):
            lineToWrite += digitsLine[bigDigitsIndexes[minutes]:bigDigitsIndexes[minutes+1]]
            lineToWrite += "                     "
        if(tensPlace>0 or minutes>1):
            lineToWrite += digitsLine[bigDigitsIndexes[tensPlace]:bigDigitsIndexes[tensPlace+1]]
        lineToWrite += digitsLine[bigDigitsIndexes[onesPlace]:bigDigitsIndexes[onesPlace+1]]
        lineToWrite += digitsLine[bigDigitsIndexes[10]:bigDigitsIndexes[11]] #add in my decimal
        lineToWrite += digitsLine[bigDigitsIndexes[tenths]:bigDigitsIndexes[tenths+1]]
        if(showJiffies):
            lineToWrite += digitsLine[bigDigitsIndexes[hundredths]:bigDigitsIndexes[hundredths+1]]
        window.addstr(i,1,lineToWrite)
        i += 1
    

def main(stdscr):
    windowArray = initializeWindows(stdscr)
    resizeWindows(windowArray)
    refreshWindows(windowArray)
    mainInput = windowArray[1].getkey() # wait for ch input from user
    processMainInput(mainInput,windowArray)
    exit = windowArray[1].getkey() # wait for ch input from user
curses.wrapper(main)
