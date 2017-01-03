import sqlite3
import os
class dbO:
    def __init__(self):
        self.connectToDataBase()

    def connectToDataBase(self):
        requiredDbPath = self.getResourcePath()
        if(os.path.isfile(requiredDbPath)):
            self.db = sqlite3.connect(requiredDbPath)
        else:
            self.db = self.createDb(requiredDbPath)

    def getResourcePath(self):
        pathOfResources = os.path.dirname(os.path.abspath(__file__))
        requiredDbPath = pathOfResources + "/times.db"
        return requiredDbPath

    def createDb(self,requiredDbPath):
        db = sqlite3.connect(requiredDbPath)
        db.execute("""CREATE TABLE SESSIONS(
                        sessionNumber INTEGER PRIMARY KEY,
                        name TEXT);""")
        db.execute("""CREATE TABLE TIMES(
                        number INTEGER,
                        session INT NOT NULL,
                        time REAL,
                        plusTwo INTEGER,
                        date TEXT,
                        scramble TEXT,
                        ao5 REAL,
                        ao12 REAL,
                        avg REAL,
                        FOREIGN KEY (session) REFERENCES SESSIONS (sessionNumber));""")
        return db
    def deliverDb(self,sessionNumber):
        retObj = []
        sessionNumber = (int(sessionNumber),)
        dbCurs = self.db.execute("""SELECT time,number,plusTwo FROM TIMES WHERE session=? ORDER BY number DESC LIMIT 20 ;""",sessionNumber)
        for record in dbCurs: 
            retObj.append(record)
        return retObj

    def addSession(self,number,name):
        #TODO reject duplicate names
        number = int(number)
        self.db.execute("INSERT INTO SESSIONS VALUES (?,?);",(number,name))
        self.db.commit()

    def getAllSessionNames(self):
        allSessionNames = {} 
        dbCurs = self.db.execute("""SELECT * FROM SESSIONS ORDER BY sessionNumber ASC;""")
        for record in dbCurs:
            name = str(record[0])
            value = str(record[1],'utf-8')
            allSessionNames[name] = value 
        return allSessionNames

    def writeDb(self,solve):
        sessionSoFar = self.deliverDb(solve['session'])
        number = self.getNumber(sessionSoFar)
        ao5,ao12,avg = self.getAverages(sessionSoFar,solve['time'])
        self.db.execute("INSERT INTO TIMES VALUES (?,?,?,?,?,?,?,?,?);",(number,solve['session'],solve['time'],solve['plusTwo'],solve['date'],solve['scramble'],ao5,ao12,avg))
        self.db.commit()
    def getNumber(self,sessionSoFar):
        try:
            number = int(sessionSoFar[0][1]) + 1
        except (TypeError,IndexError): #when empty
            number = 1
        return number
    def getAverages(self,sessionSoFar,newTime):
        ao5List = []
        ao5List.append(newTime)
        ao12List = []
        ao12List.append(newTime)
        numberOfRecords = len(sessionSoFar)
        if numberOfRecords >= 4:
            if numberOfRecords >= 11:
                for i in range(0,11):
                        ao12List.append(sessionSoFar[i][0])
                        ao5List.append(sessionSoFar[i][0])
                ao12List.sort()
                del ao12List[11]
                del ao12List[0]
                ao12 = sum(ao12List) / float(len(ao12List))
            else:
                ao12 = 0
                for i in range(0,4):
                        ao5List.append(sessionSoFar[i][0])
            ao5List.sort()
            del ao5List[4]
            del ao5List[0]
            ao5 = sum(ao5List) / float(len(ao5List))
        else:
            ao5 = 0
            ao12 = 0
        average = 1
        return ao5,ao12,average
