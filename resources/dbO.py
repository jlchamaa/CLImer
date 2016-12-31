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
    def deliverDb(self,seshName):
        retObj = []
        sessionName = (seshName,)
        dbCurs = self.db.execute("""    SELECT time , plusTwo FROM TIMES  
                                            WHERE session=?;""",sessionName)
        for record in dbCurs: 
            retObj.append(record)
        return retObj

    def addSession(self,name):
        #TODO reject duplicate names
        self.db.execute("INSERT INTO SESSIONS (name) VALUES (?);",(name,))
        self.db.commit()

    def getAllSessionNames(self):
        allSessionNames = []
        dbCurs = self.db.execute("""SELECT DISTINCT name FROM SESSIONS;""")
        for record in dbCurs:
            allSessionNames.append(str(record[0],'utf-8'))
        return allSessionNames

    def writeDb(self,solve):
        ao5,ao12,avg = self.getAverages(solve['session'],solve['time'])
        self.db.execute("INSERT INTO TIMES (session,time,plusTwo,date,scramble) VALUES (?,?,?,?,?)",(solve['session'],solve['time'],solve['plusTwo'],solve['date'],solve['scramble']))
        self.db.commit()
    def getAverages(self,session,newTime):
#TODO WRITE THIS FUNCTION
        average = 1
        ao12 = 1
        ao5 = 1
        return ao5,ao12,average
