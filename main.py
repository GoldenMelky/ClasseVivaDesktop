import api.handler.API_HANDLER as API_HANDLER
import json
from datetime import datetime
from PySide6.QtWidgets import QApplication, QDialog,QVBoxLayout,QLabel
from PySide6.QtCore import QTimer, QDate
from qt.QtWindows import LoginWindow 
from qt.QtWindows import MainWindow
import sys
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
            self.user = API_HANDLER.Utente(username,password)
            with open(CREDENZIALI_JSON, "w") as file:
                creds = {"username":username,"password":password}
                file.write(str(json.dumps(creds)))
                self.window.close()
        except Exception as e:
            if "HTTPSConnectionPool" in str(e):
                errorDialog = QDialog()
                errorDialog.setWindowTitle("ClasseViva")
                errorDialogLayout = QVBoxLayout()
                errorLabel = QLabel("Nessuna connessione ad internet, collegati e riprova.")
                errorDialogLayout.addWidget(errorLabel)
                errorDialog.setLayout(errorDialogLayout)
                errorDialog.exec()
                quit()
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
                self.window.set_tab(note(self.user),"today")

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
            "type": "Lezioni"
        })
    compiti = user.agenda(data)
    for evento in compiti["agenda"]:
        if evento["subjectDesc"]:
            title = evento["subjectDesc"]
            subtitle = evento['authorName']
        else:
            title = evento['authorName']
        output.append({
            "title": title,
            "notes": evento['notes'],
            "type": "Compiti"
        })
    note = user.note()
    for type in note:
        for nota in note[type]:
            if nota["evtDate"] == f"{'-'.join(map(str,(data[:4],data[4:6],data[6:])))}":
                output.append({
                    "title": dict_note[type],
                    "subtitle": nota["authorName"],
                    "notes": nota["evtText"],
                    "type": "Note"
                })
    return output

def note(user):
    note = user.note()
    output = []
    for type in note:
        for nota in note[type]:
            output.append({
                "title": dict_note[type],
                "subtitle": f'{nota["authorName"]} - {nota["evtDate"]}',
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
        app = QApplication(sys.argv)
        main = main()  # considera rinominare la classe in MainApp per chiarezza

        # Avvia il listener da console in un thread separato

        app.exec()


# SONO ATTUALMENTE LE 01:23 AM E STO IPLEMENTANDO IL LOGGING QUI NON SO PERCHÈ :3

