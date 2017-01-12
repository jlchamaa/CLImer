import sqlite3
import os
class dbO:
    def __init__(self):
        self.connectToDataBase()

    def connectToDataBase(self):
        requiredDbPath = self.getResourcePath()
        if(os.path.isfile(requiredDbPath)):
            self.db = sqlite3.connect(requiredDbPath)
            self.db.execute("PRAGMA foreign_keys = ON")
        else:
            self.db = self.createDb(requiredDbPath)

    def getResourcePath(self):
        pathOfResources = os.path.dirname(os.path.abspath(__file__))
        requiredDbPath = pathOfResources + "/times.db"
        return requiredDbPath

    def createDb(self,requiredDbPath):
        db = sqlite3.connect(requiredDbPath)
        db.execute("PRAGMA foreign_keys = ON")
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
                        FOREIGN KEY (session) REFERENCES SESSIONS (sessionNumber) ON DELETE CASCADE);""")
        return db

    def deliverDb(self,sessionNumber,numberOfRecords):
        retObj = []
        dbCurs = self.db.execute("""SELECT time,number,plusTwo FROM TIMES WHERE session=? ORDER BY number DESC LIMIT ?;""",(sessionNumber, numberOfRecords))
        for record in dbCurs: 
            retObj.append(record)
        return retObj

    def addSession(self,number,name):
        number = int(number)
        name = name.decode("utf-8")
        self.db.execute("INSERT INTO SESSIONS VALUES (?,?);",(number,name))
        self.db.commit()

    def deleteSession(self,session):
        self.db.execute("DELETE FROM SESSIONS WHERE sessionNumber = ?;",(session,))
        self.db.commit()

    def getAllSessionNames(self):
        allSessionNames = {} 
        dbCurs = self.db.execute("""SELECT * FROM SESSIONS ORDER BY sessionNumber ASC;""")
        for record in dbCurs:
            name = str(record[0])
            value = str(record[1])
            allSessionNames[name] = value 
        return allSessionNames

    def writeDb(self,solve):
        sessionSoFar = self.deliverDb(solve['session'],12)
        number = self.getNumber(sessionSoFar)
        ao5,ao12,avg = self.getAverages(sessionSoFar,solve['time'])
        self.db.execute("INSERT INTO TIMES VALUES (?,?,?,?,?,?,?,?,?);",(number,solve['session'],solve['time'],solve['plusTwo'],solve['date'],solve['scramble'],ao5,ao12,avg))
        self.db.commit()

    def removeRecord(self,session):
        self.db.execute("DELETE FROM TIMES WHERE session=? ORDER BY number DESC LIMIT 1;",(session,))
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
                for index,item in enumerate(ao12List):
                    if item is None:
                        ao12List[index] = float('inf')
                ao12List.sort()
                del ao12List[11]
                del ao12List[0]
                ao12 = sum(ao12List) / float(len(ao12List))
            else:
                ao12 = 0
                for i in range(0,4):
                        ao5List.append(sessionSoFar[i][0])
            for index,item in enumerate(ao5List):
                if item is None:
                    ao5List[index] = float('inf')
            ao5List.sort()
            del ao5List[4]
            del ao5List[0]
            ao5 = sum(ao5List) / float(len(ao5List))
        else:
            ao5 = 0
            ao12 = 0
        average = 1
        return ao5,ao12,average

    def plusTwo(self,session):
        recordInQuestion = self.deliverDb(session,1)
        if len(recordInQuestion) < 1:
            return
        currentPlusTwo = recordInQuestion[0][2]
        number = recordInQuestion[0][1]
        if currentPlusTwo :
            newTime = recordInQuestion[0][0] - 2
        else:
            newTime = recordInQuestion[0][0] + 2
        plusTwo = True
        self.db.execute("UPDATE TIMES SET time = ? , plusTwo = ? WHERE number = ?;",(newTime,not currentPlusTwo,number))
        self.db.commit()

    def DNF(self,session):
        recordInQuestion = self.deliverDb(session,1)
        number = recordInQuestion[0][1]
        currentlyDNF = ( recordInQuestion[0][0] == None )
        if currentlyDNF: 
            self.db.rollback()
        else:
            self.db.execute("UPDATE TIMES SET time = ? WHERE number = ?;",(None,number))
