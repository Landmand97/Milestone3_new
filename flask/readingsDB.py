import sqlite3
import threading


class readingsDB:
    lockDB= threading.Lock() #for later purposes.... Maybe

    def createDBTables(self):
        self.lockDB.acquire()
        # Opretter en forbindelse til en sqlite database (fil)
        conn = sqlite3.connect("./db.db")
        
        # reset database
        conn.execute('''DROP TABLE IF EXISTS CO2''')
        conn.execute('''DROP TABLE IF EXISTS TVOC''')
        
        # Opretter vores tabel hvis den ikke eksisterer
        conn.execute('''CREATE TABLE IF NOT EXISTS CO2 (
            Reading INTEGER, Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);''')
        conn.execute('''CREATE TABLE IF NOT EXISTS TVOC (
            Reading INTEGER, Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);''')
        conn.close()
        self.lockDB.release()

    def postReadingsToDB(self, reading):
        self.lockDB.acquire()
    
        conn = sqlite3.connect("./db.db")
        conn.execute("INSERT INTO CO2 (Reading) VALUES (?)", (reading['CO2'],))
        conn.execute("INSERT INTO TVOC (Reading) VALUES (?)", (reading['TVOC'],))

        conn.commit()
        conn.close()
        self.lockDB.release()

    def printReadings(self, sensor):
        
        conn = sqlite3.connect("db.db")
        element = []
        for row in conn.execute("SELECT * FROM {} LIMIT 100;".format(sensor)):
            #print(row)
            element.append((row))
        conn.close()
        
        return element




