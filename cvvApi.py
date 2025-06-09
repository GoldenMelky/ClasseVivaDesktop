import requests
import json

apiUrl= "https://web.spaggiari.eu/rest/"
headers = {
    "content-type": "application/json",
    "Z-Dev-ApiKey": "Tg1NWEwNGIgIC0K",
    "User-Agent": "CVVS/std/4.1.7 Android/10"
}



class Utente:
    def __init__(self, username: str = "", password: str = ""):
        if username == "" or password == "":
            raise ValueError("Username and password cannot be empty.")
        self.username = username
        self.password = password
        endpoint = apiUrl + "v1/auth/login"
        body=f'{{"ident": null, "pass": "{self.password}", "uid": "{self.username}"}}'
        self.login = json.loads(requests.post(endpoint, data=body, headers=headers).text)
        self.login.update({"studendId": self.username[1:-1]})
        headers.update({"Z-Auth-Token": self.login["token"]})
        self.headers = headers
        print(f'Logged as: {" ".join([self.login[key] for key in ["firstName", "lastName"]])}')
    
    def agenda(self,begin: str, end: str = ""):
        if end == "":
            end = begin
        endpoint = apiUrl + f"v1/students/{self.login["studendId"]}/agenda/all/{begin}/{end}"
        response = requests.get(endpoint, headers=self.headers)
        return json.loads(response.text)
    def assenze(self):
        endpoint = apiUrl + f"v1/students/{self.login['studendId']}/absences/details"
        response = requests.get(endpoint, headers=self.headers)
        return json.loads(response.text)
    def didattica(self, contentId: str = ""):
        endpoint = apiUrl + f"v1/students/{self.login['studendId']}/didactics"
        if contentId:
            endpoint = endpoint + "/item/" + contentId
        response = requests.get(endpoint, headers=self.headers)
        return json.loads(response.text)
    def bacheca(self):
        endpoint = apiUrl + f"v1/students/{self.login['studendId']}/noticeboard"
        response = requests.get(endpoint, headers=self.headers)
        return json.loads(response.text)
    def libri(self):
        endpoint = apiUrl + f"v1/students/{self.login['studendId']}/schoolbooks"
        response = requests.get(endpoint, headers=self.headers)
        return json.loads(response.text)
    def voti(self):
        endpoint = apiUrl + f"v1/students/{self.login['studendId']}/grades"
        response = requests.get(endpoint, headers=self.headers)
        print(response.text)
        return json.loads(response.text)
    def note(self):
        endpoint = apiUrl + f"v1/students/{self.login['studendId']}/notes/all"
        response = requests.get(endpoint, headers=self.headers)
        return json.loads(response.text)
    def periodi(self):
        endpoint = apiUrl + f"v1/students/{self.login['studendId']}/periods"
        response = requests.get(endpoint, headers=self.headers)
        return json.loads(response.text)
    def materie(self):
        endpoint = apiUrl + f"v1/students/{self.login['studendId']}/subjects"
        response = requests.get(endpoint, headers=self.headers)
        return json.loads(response.text)
    def documenti(self):
        endpoint = apiUrl + f"v1/students/{self.login['studendId']}/documents"
        response = requests.get(endpoint, headers=self.headers)
        return json.loads(response.text)
    def lezioni(self, begin: str, end: str = ""):
        if end == "":
            end = begin
        endpoint = apiUrl + f"v1/students/{self.login['studendId']}/lessons/{begin}/{end}"
        response = requests.get(endpoint, headers=self.headers)
        return json.loads(response.text)
