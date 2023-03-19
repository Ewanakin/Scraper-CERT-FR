import mysql.connector
class BddVulnerablilite:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.mydb = ""

    # initialisation de la connexion
    def CreateConnexion(self):
        try:
            self.mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            return True
        except:
            return False


    def checkCVE(self, cve):
        cursor = self.mydb.cursor()
        req = ("SELECT id FROM vulnerability WHERE cve = %s")
        cursor.execute(req, (cve,))
        if cursor.fetchone() == None:
            return True
        else:
            return False

    def insertCVE(self, cve, link, vulnType):
        if self.checkCVE(cve):
            cursor = self.mydb.cursor()
            req = ("INSERT INTO vulnerability(cve, link, discr) VALUES(%s,%s,%s)")
            data = (cve, link, vulnType)
            cursor.execute(req, data)
            self.mydb.commit()
            req = ("SELECT id FROM vulnerability WHERE cve = %s")
            cursor.execute(req, (cve,))
            idVuln = cursor.fetchone()
            req = ("INSERT INTO "+vulnType+"(id) VALUES(%s)")
            data = (idVuln)
            cursor.execute(req, data)
            self.mydb.commit()
            cursor.close()
            return True
        else :
            return False