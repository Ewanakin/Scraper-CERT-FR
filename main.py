import requests
from bs4 import BeautifulSoup

def getCVE(url, soup, alertType):
    for element in soup.find_all('div', attrs={"class": alertType}):
        for link in element.find_next("a"):
            match alertType:
                case "cert-alert":
                    print(url+"alerte/"+link.text)
                    pass
                case "cert-avis":
                    print(url+"avis/"+link.text)

url = "https://www.cert.ssi.gouv.fr/"

if __name__ == '__main__':
    page = requests.get(url).text
    soup = BeautifulSoup(page, "html.parser")
    # récupération des alertes du cert
    getCVE(url, soup, "cert-alert")
    # récupération des avis du cert
    getCVE(url, soup, "cert-avis")

