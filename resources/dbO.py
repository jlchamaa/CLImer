import sqlite3
import os
class dbO:
    def __init__(self):
        pathOfResources = os.path.dirname(os.path.abspath(__file__))
        requiredDbPath = pathOfResources + "/times.db"
        if(os.path.isfile(requiredDbPath)):
            self.db = sqlite3.connect(requiredDbPath)
        else:
            self.db = self.createDb(requiredDbPath)

    def createDb(self,requiredDbPath):
        db = sqlite3.connect(requiredDbPath)
        db.execute("""CREATE TABLE SESSIONS(
                        sessionNumber INTEGER PRIMARY KEY,
                        name TEXT);""")
        db.execute("""CREATE TABLE TIMES(
                        number INTEGER,
                        time REAL,
                        ao5 REAL,
                        ao12 REAL,
                        avg REAL,
                        plusTwo INTEGER,
                        date TEXT,
                        scramble TEXT,
                        session INT NOT NULL,
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

    def getAllSessionNames(self):
        allSessionNames = []
        dbCurs = self.db.execute("""    SELECT DISTINCT session FROM TIMES
        """)
        for record in dbCurs:
            allSessionNames.append(str(record[0]))
        return allSessionNames

    def writeDb(self,solve):
        self.db.execute("INSERT INTO TIMES VALUES (?,?,?,?,?)",(solve['session'],solve['time'],solve['plusTwo'],solve['date'],solve['scramble']))
        self.db.commit()
