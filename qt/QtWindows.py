from PySide6.QtWidgets import QDateEdit, QApplication, QMainWindow, QLineEdit, QVBoxLayout,QHBoxLayout, QLabel, QWidget, QPushButton, QCalendarWidget, QGridLayout,QToolButton, QFrame, QScrollArea
from PySide6.QtCore import Signal, Qt, QSize, QDate
from PySide6.QtGui import QPixmap, QPalette, QIcon
from datetime import date
from qt.tabs import *

#########################################
#              SETTINGS                 #
#########################################


class LoginWindow(QMainWindow):
    login_attempt = Signal(str, str)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        
        username_label = QLabel(text="Username")
        self.username_entry = QLineEdit()
        self.username_entry.returnPressed.connect(self.login)
        username_layout = QHBoxLayout()
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_entry)

        password_label = QLabel(text="Password")
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.returnPressed.connect(self.login)
        password_layout = QHBoxLayout()
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_entry)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: #ed4337;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout = QVBoxLayout()
        layout.addLayout(username_layout)
        layout.addLayout(password_layout)
        layout.addWidget(login_button)
        layout.addWidget(self.error_label)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)   
        self.adjustSize()
        self.setFixedSize(self.size())  

    def login(self):
        username = self.username_entry.text()
        password = self.password_entry.text()
        self.login_attempt.emit(username,password)

    def resize(self):
        self.setMaximumSize(16777215, 16777215)
        self.adjustSize()
        self.setFixedSize(self.size())  

class MainWindow(QMainWindow):
    icon_paths = [
        "data/icons/today.svg",
        "data/icons/agenda.svg",
        "data/icons/lezioni.svg",
        "data/icons/voti.svg",
        "data/icons/note.svg"
    ]
    sidebar_clicked = Signal(str,str)

    
    def clear_tab(self):
        while self.layout.count() > 1:
            item = self.layout.takeAt(1)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
        self.loading = QLabel("loading...")
        self.layout.addWidget(self.loading)
    
    def set_tab(self,list, tab):
        self.loading.deleteLater()
        match tab:
            case "today":
                tab_widget = today_tab(list,self.selected_date)
                tab_widget.sidebar_clicked.connect(self.sidebar_clicked.emit)
                self.layout.addWidget(tab_widget)
                

    def __init__(self):
        super().__init__()
        self.selected_date = QDate.currentDate()
        self.setWindowTitle("ClasseViva")
        self.setBackgroundRole
        iconbar_layout = QVBoxLayout()
        for iconpath in self.icon_paths:
            btn = QToolButton()
            icon=QIcon(iconpath)
            btn.setFixedSize(40,40)
            btn.setIcon(icon)
            btn.setIconSize(btn.size())
            #btn.setStyleSheet("background: transparent; border: none;")
            btn.setFocusPolicy(Qt.NoFocus)
            btn.setObjectName(iconpath.split("/")[-1].split(".")[0])
            btn.clicked.connect(lambda checked, b=btn: self.sidebar_clicked.emit(b.objectName(),""))
            iconbar_layout.addWidget(btn)
        iconbar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)




        setting_layout = QVBoxLayout()
        sett = QToolButton()
        icon=QPixmap("data/icons/menu.svg")
        sett.setFixedSize(40,40)
        sett.setIcon(icon)
        sett.setIconSize(btn.size())
        #sett.setStyleSheet("background: transparent; border: none;")
        sett.setFocusPolicy(Qt.NoFocus)


        setting_layout.addWidget(sett)
        setting_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)

        sidebar_layout = QVBoxLayout()
        sidebar_layout.addLayout(iconbar_layout)
        sidebar_layout.addLayout(setting_layout)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        sidebar = QWidget()
        sidebar.setLayout(sidebar_layout)
        sidebar.setFixedWidth(sidebar.sizeHint().width())

        

        self.layout:QHBoxLayout = QHBoxLayout()
        self.layout.addWidget(sidebar)
        self.layout.addWidget(QLabel("Click any icon"))
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        self.resize(600,400)

        # widget (QWidget)                                                      #   widget principale
        #   └── self.layout (QHBoxLayout)                                       #   layout
        #         ├── sidebar (QWidget)                                         #   barra laterale
        #         │     └── sidebar_layout (QVBoxLayout)                        #   layout della barra laterale
        #         │           ├── iconbar_layout (QVBoxLayout)                  #   layout delle icone
        #         │           │     └── btn (QToolButton × n)                   #   icone
        #         │           └── setting_layout (QVBoxLayout)                  #   layout del hamburger menu
        #         │                 └── sett (QToolButton)                      #   menu
        #         └── self.right_bar (QVBoxLayout)                                   #   
        #             └── tab_scroll (QScrollArea)                           #   
        #                   └── tab_widget (QWidget)                         #
        #                         └── self.tab (QVBoxLayout)                 #
        #                               └── frame (QFrame × n)                  #
        #                                     └── frame_layout (QVBoxLayout)    #
        #                                           ├── title (QLabel)          #
        #                                           └── subtitle (QLabel)       #
        #outdated