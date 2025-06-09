import cvvApi
from tkinter import ttk
from tkinter import *
from tkcalendar import *
import json
from datetime import datetime
from threading import Thread
from time import sleep
from PIL import Image, ImageTk

splash = Tk()
frame = Frame(splash, background="#e40b29")
frame.pack(fill=BOTH, expand=True)
splash.title("Login...")
splash.geometry("317x150")
spalshImage = ImageTk.PhotoImage(Image.open("classevivaSplash.png").resize((317, 100)))
panel = Label(frame, image=spalshImage, background="#e40b29")
panel.pack()
loginLabel = Label(frame, text="Login in corso...", background="#e40b29", foreground="white", font=(16))
loginLabel.pack()


def loginButton():
    password = password_entry.get()
    username = username_entry.get()
    try:
        global user 
        user = loginFunc(username, password)
        login.destroy()
    except Exception as e:
        error_label.config(text=f"Errore: {str(e)}")
        error_label.pack(pady=5)
        return

def loginFunc(username,password):
    global user
    user = cvvApi.Utente(username, password)
    loginLabel.config(text=f"Ciao {user.login["firstName"].title()}")
    with open("credenziali.json", "w") as file:
        creds = {"username":username,"password":password}
        file.write(str(json.dumps(creds)))
    splash.destroy()
    

try:
    with open("credenziali.json", "r") as file:
        creds = json.loads(file.read())
        username = creds["username"]
        password = creds["password"]
        t = Thread(target=loginFunc, args=(username, password))
        t.start()
except FileNotFoundError:
    login = Tk()
    login.attributes(topmost=True)
    login.title("Login")
    login.geometry("350x200")
    login.resizable(False, False)
    
    username = StringVar()
    password = StringVar()

    username_label = ttk.Label(login, text="Username:")
    username_label.pack(pady=5)
    username_entry = ttk.Entry(login,textvariable=username)
    username_entry.pack(pady=5)
    username_entry.focus()

    password_label = ttk.Label(login, text="Password:")
    password_label.pack(pady=5)
    password_entry = ttk.Entry(login,textvariable=password, show="*")
    password_entry.pack(pady=5)

    error_label = ttk.Label(login, text="", foreground="red")
    
    login_button = ttk.Button(login, text="Login", command=loginButton)
    login_button.pack(pady=5)
    login.mainloop()

def today(data: str=""):
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

def main():
    root = Tk()
    root.title("ClasseViva")
    root.geometry("300x200")

    # cal = Calendar(root,date_pattern="YYYYMMDD")
    # cal.pack()
    # cal.bind("<<CalendarSelected>>", lambda e: print(today(cal.get_date())))
    root.mainloop()
splash.mainloop()
#main()