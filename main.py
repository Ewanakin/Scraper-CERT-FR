import requests
from bs4 import BeautifulSoup
from BddVulnerablilite import BddVulnerablilite
import json

def getCVE(connexionBdd, url, soup, alertType):
    for element in soup.find_all('div', attrs={"class": alertType}):
        for link in element.find_next("a"):
            match alertType:
                case "cert-alert":
                    print(connexionDb.insertCVE(link.text, url+"alerte/"+link.text, "alerte"))
                case "cert-avis":
                    print(connexionDb.insertCVE(link.text, url+"avis/"+link.text, "avis"))

url = "https://www.cert.ssi.gouv.fr/"

if __name__ == '__main__':
    with open("config.json") as file:
        data = json.load(file)
        host = data["host"]
        username = data["username"]
        password = data["password"]
        database = data["database"]
        connexionDb = BddVulnerablilite(host, username, password, database)
        if connexionDb.CreateConnexion():
            checkConnexion = True
        else:
            checkConnexion = False
    if checkConnexion:
        page = requests.get(url).text
        soup = BeautifulSoup(page, "html.parser")
        # récupération des alertes du cert
        getCVE(connexionDb, url, soup, "cert-alert")
        getCVE(connexionDb, url, soup, "cert-avis")

