import cvvApi
import tkinter as tk
import json

with open("credenziali.json", "r") as file:
    creds = json.loads(file.read())
    username = creds["username"]
    password = creds["password"]

user = cvvApi.Utente(username, password)

def today(data: str=""):
    output = []
    lezioni = user.lezioni(data)
    for lezione in lezioni["lessons"]:
        if lezione["subjectDesc"]:
            title = lezione["subjectDesc"]
            subtitle = lezione['authorName'] + " - "
        else:
            title = lezione['authorName']
            subtitle = ""
        subtitle += f"{lezione["evtHPos"]}° ora"
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
    for i in note.values():
        for nota in i:
            if nota["evtDate"] == f"{'-'.join(map(str,(data[:4],data[4:6],data[6:])))}":
                output.append({
                    "title": nota["authorName"],
                    "subtitle": nota["evtDate"],
                    "notes": nota["evtText"],
                    "type": "nota"
                })
    return output

def note():
    note = user.note()
    output = []
    for i in note.values():
        for nota in i:
            output.append({
                "title": nota["authorName"],
                "subtitle": nota["evtDate"],
                "notes": nota["evtText"]
            })
    return output

def voti():
    voti = user.voti()
    output = []
    for voto in voti["grades"]:
        output.append({
            "title": voto["subjectDesc"],
            "subtitle": voto["displayValue"] + " - " + voto["evtDate"],
            "notes": voto["notesForFamily"]
        })
    return output

window = tk.Tk()
window.title("CVV Desktop")
window.geometry("600x400")
first_button = tk.Button(text="Saluta!", command=voti)
first_button.grid(row=0, column=0, sticky="WE")
irst_button = tk.Button(text="Saluta!", command=voti)
irst_button.grid(row=1, column=1)
window.columnconfigure(0, weight=3)
window.mainloop()