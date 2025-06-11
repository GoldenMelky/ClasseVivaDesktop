import requests  # Libreria per effettuare richieste HTTP
import json      # Libreria per lavorare con dati JSON

apiUrl = "https://web.spaggiari.eu/rest/"  # URL base dell'API ClasseViva
headers = {
    "content-type": "application/json",  # Specifica il tipo di contenuto delle richieste
    "Z-Dev-ApiKey": "Tg1NWEwNGIgIC0K",   # Chiave API richiesta dal servizio
    "User-Agent": "CVVS/std/4.1.7 Android/10"  # User-Agent richiesto dall'API
}

class Utente:
    def __init__(self, username: str = "", password: str = ""):
        # Controlla che username e password siano forniti
        if username == "" or password == "":
            raise ValueError("Username and password cannot be empty.")
        self.username = username
        self.password = password
        endpoint = apiUrl + "v1/auth/login"  # Endpoint per il login
        body = json.dumps({
            "ident": None,
            "pass": self.password,
            "uid": self.username
        })
        # Effettua una richiesta POST all'endpoint di login con le credenziali fornite
        req = requests.post(endpoint, data=body, headers=headers)
        if "WrongCredentials" in req.text:
            raise ValueError("Wrong username or password.")
        self.login = json.loads(req.text)  # Salva la risposta del login
        self.login.update({"studentId": self.username[1:-1]})  # Estrae lo studentId dallo username
        headers.update({"Z-Auth-Token": self.login["token"]})  # Aggiorna l'header con il token di autenticazione
        self.headers = headers.copy()  # Salva gli header aggiornati per le richieste successive
        print(f'Logged as: {" ".join([self.login[key] for key in ["firstName", "lastName"]])}')
    
    def agenda(self, begin: str, end: str = ""):
        # Recupera l'agenda tra due date (o una sola se end non è fornito)
        if end == "":
            end = begin
        endpoint = apiUrl + f"v1/students/{self.login['studentId']}/agenda/all/{begin}/{end}"
        response = requests.get(endpoint, headers=self.headers)
        return json.loads(response.text)

    def assenze(self):
        # Recupera i dettagli delle assenze
        endpoint = apiUrl + f"v1/students/{self.login['studentId']}/absences/details"
        response = requests.get(endpoint, headers=self.headers)
        return json.loads(response.text)

    def didattica(self, contentId: str = ""):
        # Recupera i materiali didattici, opzionalmente un contenuto specifico
        endpoint = apiUrl + f"v1/students/{self.login['studentId']}/didactics"
        if contentId:
            endpoint = endpoint + "/item/" + contentId
        response = requests.get(endpoint, headers=self.headers)
        return json.loads(response.text)

    def bacheca(self):
        # Recupera i messaggi della bacheca
        endpoint = apiUrl + f"v1/students/{self.login['studentId']}/noticeboard"
        response = requests.get(endpoint, headers=self.headers)
        return json.loads(response.text)

    def libri(self):
        # Recupera i libri scolastici associati allo studente
        endpoint = apiUrl + f"v1/students/{self.login['studentId']}/schoolbooks"
        response = requests.get(endpoint, headers=self.headers)
        return json.loads(response.text)

    def voti(self):
        # Recupera i voti dello studente
        endpoint = apiUrl + f"v1/students/{self.login['studentId']}/grades"
        response = requests.get(endpoint, headers=self.headers)
        return json.loads(response.text)

    def note(self):
        # Recupera le note 
        # NTTE Annotazione del docente 
        # NTCL Nota disciplinare
        # NTWN Richiamo
        endpoint = apiUrl + f"v1/students/{self.login['studentId']}/notes/all"
        response = requests.get(endpoint, headers=self.headers)
        return json.loads(response.text)

    def periodi(self):
        # Recupera i periodi scolastici
        endpoint = apiUrl + f"v1/students/{self.login['studentId']}/periods"
        response = requests.get(endpoint, headers=self.headers)
        return json.loads(response.text)

    def materie(self):
        # Recupera le materie dello studente
        endpoint = apiUrl + f"v1/students/{self.login['studentId']}/subjects"
        response = requests.get(endpoint, headers=self.headers)
        return json.loads(response.text)

    def documenti(self):
        # Recupera i documenti associati allo studente
        endpoint = apiUrl + f"v1/students/{self.login['studentId']}/documents"
        response = requests.get(endpoint, headers=self.headers)
        return json.loads(response.text)

    def lezioni(self, begin: str, end: str = ""):
        # Recupera le lezioni tra due date (o una sola se end non è fornito)
        if end == "":
            end = begin
        endpoint = apiUrl + f"v1/students/{self.login['studentId']}/lessons/{begin}/{end}"
        response = requests.get(endpoint, headers=self.headers)
        return json.loads(response.text)
