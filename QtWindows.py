from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout,QHBoxLayout, QLabel, QWidget, QPushButton
from PySide6.QtCore import Signal, Qt, QSize

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
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ClasseViva")
        
        