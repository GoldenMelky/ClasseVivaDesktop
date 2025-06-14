import api.handler.API_HANDLER as API_HANDLER
import json
from datetime import datetime
from threading import Thread
from time import sleep
from PIL import Image, ImageTk
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QColor
from PySide6.QtCore import QTimer, QDate
from qt.QtWindows import LoginWindow 
from qt.QtWindows import MainWindow
import sys
import logging
import configparser
import os

#########################################
#              SETTINGS                 #
#########################################
CONFIG_FILE = "data/config.conf"

config = configparser.ConfigParser()

# Create default config if not exists
if not os.path.exists(CONFIG_FILE):
    config['DEFAULT'] = {
        'data_dir': 'data/',
        'credenziali_file': 'data/credenziali.json'
    }
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
else:
    config.read(CONFIG_FILE)

DATA = config['DEFAULT'].get('data_dir', 'data/')
CREDENZIALI_JSON = config['DEFAULT'].get('credenziali_file', 'data/credenziali.json')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

#########################################
#              MAIN CLASS               #
#########################################
class main():

    def __init__(self):
        self.user = None
        self.getCredentials()
        self.startMainWindow()

    def startMainWindow(self):
        self.window = MainWindow()
        self.window.show()
        self.window.sidebar_clicked.connect(self.sidebar_clicked)


    #########################################
    #              LOGIN LOGIC              #
    #########################################
    # Tenta il login, se va a buon fine aggiorna le credenziali in credenziali.json, sennò da errore all'utente
    def login(self,username,password): # VICCCC DEVI SCRIVERE I COMMENTI, STO FACEDO IL REVERSE DI UN PROGRAMMA A CUI HO ACCESSO AL SC 
        try:
            if os.path.exists(CREDENZIALI_JSON):
                logging.info('LOG | Credentials file already exists. Skipping login.')

            self.user = API_HANDLER.Utente(username,password)
            with open(CREDENZIALI_JSON, "w") as file:
                creds = {"username":username,"password":password}
                file.write(str(json.dumps(creds)))
                self.window.close()
                logging.info('LOG | 200 OK, SAVED')
        except Exception as e:
            self.window.error_label.setText(str(e))
            QTimer.singleShot(0,self.window.resize)  # aggiorna la larghezza della finestra

    #########################################
    #        CREDENTIALS MANAGEMENT         #
    #########################################
    # Ottiene le credenziali, se non sono salvate le chiede all'utente
    def getCredentials(self):
        self.window = LoginWindow()
        try:
            with open(CREDENZIALI_JSON, "r") as file:
                creds = json.loads(file.read())
                username = creds["username"]
                password = creds["password"]
                self.login(username,password)
                
                logging.info("LOG | 200 OK, LOGGED IN")
        except FileNotFoundError:
            self.window.show()
            self.window.login_attempt.connect(self.login)
    
    #########################################
    def sidebar_clicked(self, btn, date=""):
        self.window.clear_tab()
        match btn:
            case "today":
                if date:
                    self.window.selected_date = QDate.fromString(date, "yyyyMMdd")
                self.window.set_tab(today(self.user, date),"today")
            case "note":
                self.window.set_tab(note(self.user),"Note")

dict_note={
        "NTTE": "Annotazione",
        "NTCL":"Nota disciplinare",
        "NTWN":"Richiamo" 
    }
#########################################
#           DATA RETRIEVAL UTILS        #
#########################################
# Restituisce una lista di lezioni, compiti e note del giorno dato
def today(user: API_HANDLER.Utente, data: str=""):
    if not data:
        data = datetime.now().strftime("%Y%m%d")
    output = []
    lezioni = user.lezioni(data)
    for lezione in lezioni["lessons"]:
        if lezione["subjectDesc"]:
            title = lezione["subjectDesc"]
            subtitle = lezione['authorName'] + " - "
        else:
            title = lezione['authorName']
            subtitle = ""
        subtitle += f"{lezione['evtHPos']}° ora"
        output.append({
            "title": title,
            "subtitle": subtitle,
            "notes": lezione['lessonArg'],
            "type": "lezione"
        })
    compiti = user.agenda(data)
    for evento in compiti["agenda"]:
        if evento["subjectDesc"]:
            title = evento["subjectDesc"]
            subtitle = evento['authorName'] + " - "
        else:
            title = evento['authorName']
            subtitle = ""
        subtitle += f"{evento['evtDatetimeBegin'].split('T')[1].split('+')[0][:-3]}-{evento['evtDatetimeEnd'].split('T')[1].split('+')[0][:-3]}"
        output.append({
            "title": title,
            "subtitle": subtitle,
            "notes": evento['notes'],
            "type": "compito"
        })
    note = user.note()
    for type in note:
        for nota in note[type]:
            if nota["evtDate"] == f"{'-'.join(map(str,(data[:4],data[4:6],data[6:])))}":
                output.append({
                    "title": nota["authorName"],
                    "subtitle": dict_note[type],
                    "notes": nota["evtText"],
                    "type": "nota"
                })
    return output

def note(user):
    note = user.note()
    output = []
    for type in note:
        for nota in note[type]:
            output.append({
                "title": nota["authorName"],
                "subtitle": f'{nota["evtDate"]} - {dict_note[type]}',
                "notes": nota["evtText"],
                "type": dict_note[type]
            })
    return output

def voti(user):
    voti = user.voti()
    output = []
    for voto in voti["grades"]:
        output.append({
            "title": voto["subjectDesc"],
            "subtitle": voto["displayValue"] + " - " + voto["evtDate"],
            "notes": voto["notesForFamily"]
        })
    return output

#########################################
#              MAIN ENTRY               #
#########################################
if __name__ == "__main__":
    def console_listener():
        while True:
            cmd = input(">> ").strip()
            if cmd.lower() == "exit":
                logging.info("LOG | Exit command received. Closing app.")
                QApplication.quit()
                break

    try:
        app = QApplication(sys.argv)
        main = main()  # considera rinominare la classe in MainApp per chiarezza

        # Avvia il listener da console in un thread separato
        Thread(target=console_listener, daemon=True).start()

        app.exec()
    except KeyboardInterrupt:
        logging.warning("KeyboardInterrupt | Manual shutdown detected.")


# SONO ATTUALMENTE LE 01:23 AM E STO IPLEMENTANDO IL LOGGING QUI NON SO PERCHÈ :3

