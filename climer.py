from resources.digits import bigDigits,bigDigitsIndexes
from resources import dbO
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
        timer(windowArray[1])
        return True
    elif(inputKey == 'e'):
        return False
    else:
        refreshWindows(windowArray)
        return True

def timer(window):
    window.nodelay(1)
    d="p" # not space
    curtime=0
    start = time.time()
    while(d!=32 and d!=27): #character for space
        now = time.time()
        tick = round(now-start,2) 
        if(curtime!=tick):
            curtime=tick
            drawTime(curtime,window)
        d=window.getch()
    window.nodelay(0)
    #writeDb(dbCursor,session,curtime,0,)
def drawTime(time,window):
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
        lineToWrite += fetchDigitChunk(digitsLine,tenmins,time<600) #tens place of mins
        lineToWrite += fetchDigitChunk(digitsLine,minutes,time<60) #singles of mins 
        lineToWrite += fetchDigitChunk(digitsLine,11,time<60) # add colon
        lineToWrite += fetchDigitChunk(digitsLine,tensPlace,time<10) # add tensPlace
        lineToWrite += fetchDigitChunk(digitsLine,onesPlace,time<1) # add tensPlace
        lineToWrite += fetchDigitChunk(digitsLine,10,False) # add tensPlace
        lineToWrite += fetchDigitChunk(digitsLine,tenths,False) # add tensPlace
        lineToWrite += fetchDigitChunk(digitsLine,hundredths,False) # add tensPlace
        window.addstr(i,15,lineToWrite)
        i += 1
def fetchDigitChunk(line,number,empty):
# 10 gets .   11 get : 
    if empty:
        size = bigDigitsIndexes[number+1]-bigDigitsIndexes[number]
        space = ""
        for i in range(0,size):
            space += " "
        return space
    else:
        return  line[bigDigitsIndexes[number]:bigDigitsIndexes[number+1]]


def main(stdscr):
    dbObject = dbO.dbO()
    curses.curs_set(0)
    windowArray = initializeWindows(stdscr)
    resizeWindows(windowArray)
    refreshWindows(windowArray)
    status = True;
    while status: 
        mainInput = windowArray[1].getkey() # wait for ch input from user
        status = processMainInput(mainInput,windowArray)
curses.wrapper(main)
