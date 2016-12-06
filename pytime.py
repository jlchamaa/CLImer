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
            drawTime(curtime,window)
        d=window.getch()
    #TODO add database logic

def drawTime(time,window):
    window.clear()
    integerPart = int(round(time))
    i=1
    for digitsLine in bigDigits:
        lineToWrite = digitsLine[bigDigitsIndexes[integerPart]:bigDigitsIndexes[integerPart+1]]
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
