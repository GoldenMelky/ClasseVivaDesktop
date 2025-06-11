from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout,QHBoxLayout, QLabel, QWidget, QPushButton, QCalendarWidget, QGridLayout,QToolButton, QFrame, QScrollArea
from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QPixmap, QPalette, QIcon

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
        "data/icons/agenda.svg",
        "data/icons/lezioni.svg",
        "data/icons/voti.svg",
        "data/icons/note.svg"
    ]

    sidebar_clicked = Signal(str)

    def clear_events(self):
        while self.events.count():
            widget = self.events.takeAt(0).widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

    def set_events(self, list:list):
        print(list)
        for event in list:
            frame_layout = QVBoxLayout()

            frame = QFrame()
            frame.setStyleSheet("background-color:rgba(0, 0, 0, 0.5); border-radius: 10px;")
            frame.setFrameShape(QFrame.StyledPanel)
            frame.setFrameShadow(QFrame.Raised)

            title = QLabel(event["title"])
            title.setStyleSheet("font: 15pt; background-color:rgba(0, 0, 0, 0);")
            subtitle = QLabel(event["subtitle"])
            subtitle.setStyleSheet("font:12pt;background-color:rgba(0, 0, 0, 0);")
            
            notes = QLabel(event["notes"])
            notes.setStyleSheet("background-color:rgba(0, 0, 0, 0);")
            notes.setWordWrap(True)

            frame_layout.addWidget(title)
            frame_layout.addWidget(subtitle)
            frame_layout.addWidget(notes)
            frame.setLayout(frame_layout)
            self.events.addWidget(frame)

    def __init__(self):
        super().__init__()
        
        iconbar_layout = QVBoxLayout()
        for iconpath in self.icon_paths:
            btn = QToolButton()
            icon=QPixmap(iconpath)
            btn.setFixedSize(40,40)
            btn.setIcon(icon)
            btn.setIconSize(btn.size())
            btn.setStyleSheet("background: transparent; border: none;")
            btn.setFocusPolicy(Qt.NoFocus)
            btn.setObjectName(iconpath.split("/")[-1].split(".")[0])
            btn.clicked.connect(lambda checked, b=btn: self.sidebar_clicked.emit(b.objectName()))
            iconbar_layout.addWidget(btn)
        iconbar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)




        setting_layout = QVBoxLayout()
        sett = QToolButton()
        icon=QPixmap("icons/menu.svg")
        sett.setFixedSize(40,40)
        sett.setIcon(icon)
        sett.setIconSize(btn.size())
        sett.setStyleSheet("background: transparent; border: none;")
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

        events_widget = QWidget()
        self.events = QVBoxLayout(events_widget)
        self.events.addWidget(QLabel("Click any icon"))

        events_scroll = QScrollArea()
        events_scroll.setStyleSheet("background: transparent; border: none;")
        events_scroll.setWidgetResizable(True)
        events_scroll.setWidget(events_widget)

        layout = QHBoxLayout()
        layout.addWidget(sidebar)
        layout.addWidget(events_scroll)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.resize(600,400)

        # widget (QWidget)                                                      #   widget principale
        #   └── layout (QHBoxLayout)                                            #   layout
        #         ├── sidebar (QWidget)                                         #   barra laterale
        #         │     └── sidebar_layout (QVBoxLayout)                        #   layout della barra laterale
        #         │           ├── iconbar_layout (QVBoxLayout)                  #   layout delle icone
        #         │           │     └── btn (QToolButton × n)                   #   icone
        #         │           └── setting_layout (QVBoxLayout)                  #   layout del hamburger menu
        #         │                 └── sett (QToolButton)                      #   menu
        #         └── events_scroll (QScrollArea)                               #   
        #               └── events_widget (QWidget)                             #
        #                     └── self.events (QVBoxLayout)                     #
        #                           └── frame (QFrame × n)                      #
        #                                 └── frame_layout (QVBoxLayout)        #
        #                                       ├── title (QLabel)              #
        #                                       └── subtitle (QLabel)           #