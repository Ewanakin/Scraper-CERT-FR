import requests, json, smtplib, ssl
from bs4 import BeautifulSoup
from BddVulnerablilite import BddVulnerablilite
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def sendMail(listVuln):
    with open("configMail.json") as file:
        data = json.load(file)
        sender_email = data["from"]
        receiver_email = data["to"]
        password = data["password"]
    message = MIMEMultipart("alternative")
    message["Subject"] = "new Vulnerability"
    message["From"] = sender_email
    message["To"] = receiver_email
    # Create the plain-text and HTML version of your message
    # Create the plain-text and HTML version of your message
    text = """\
    Les nouvelles vulnérabilitées : \n
    """
    for vuln in listVuln:
        text += vuln + "\n"
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

def getCVE(url, soup, alertType):
    listVuln = []
    for element in soup.find_all('div', attrs={"class": alertType}):
        for link in element.find_next("a"):
            match alertType:
                case "cert-alert":
                    if connexionDb.insertCVE(link.text, url+"alerte/"+link.text, "alerte"):
                        print("La CVE : " + link.text + " à bien été ajoutée")
                        listVuln.append(url + "alerte/" + link.text)
                    else :
                        print("La CVE : " + link.text + " est déjà enrgistrée")
                case "cert-avis":
                    if connexionDb.insertCVE(link.text, url + "avis/" + link.text, "avis"):
                        print("La CVE : " + link.text + " à bien été ajoutée")
                        listVuln.append(url + "avis/" + link.text)
                    else:
                        print("La CVE : " + link.text + " est déjà enrgistrée")
    if len(listVuln) != 0:
        sendMail(listVuln)

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
        getCVE(url, soup, "cert-alert")
        getCVE(url, soup, "cert-avis")



