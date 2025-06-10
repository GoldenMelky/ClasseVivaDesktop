from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout,QHBoxLayout, QLabel, QWidget, QPushButton, QCalendarWidget, QGridLayout,QToolButton
from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QPixmap, QPalette, QIcon


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
        "icons/agenda.svg",
        "icons/lezioni.svg",
        "icons/voti.svg",
        "icons/note.svg"
    ]
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

        events = QVBoxLayout()
        label2 = QLabel("iconbar")
        label3 = QLabel("iconbar")
        events.addWidget(label2)
        events.addWidget(label3)

        layout = QHBoxLayout()
        layout.addWidget(sidebar)
        layout.addLayout(events)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.resize(600,400)

        
        