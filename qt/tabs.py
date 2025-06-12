from PySide6.QtWidgets import QDateEdit, QApplication, QMainWindow, QLineEdit, QVBoxLayout,QHBoxLayout, QLabel, QWidget, QPushButton, QCalendarWidget, QGridLayout,QToolButton, QFrame, QScrollArea
from PySide6.QtCore import Signal, Qt, QSize, QDate
from PySide6.QtGui import QPixmap, QPalette, QIcon
from datetime import date

class today_tab(QWidget):
    sidebar_clicked = Signal(str,str)
    def __init__(self,list:list,initial_date: QDate):
        super().__init__()
        main_layout = QVBoxLayout(self)
        title_layout = QHBoxLayout()
        main_layout.addLayout(title_layout)

        tab_title = QLabel("Oggi a scuola")
        title_layout.addWidget(tab_title)
        tab_title.setStyleSheet("font: 15pt;")

        date_picker = QDateEdit()
        date_picker.setDisplayFormat("dd MMMM yyyy")
        date_picker.setDate(initial_date)
        date_picker.setCalendarPopup(True)
        date_picker.dateChanged.connect(lambda: self.sidebar_clicked.emit("today", date_picker.date().toString("yyyyMMdd")))
        title_layout.addWidget(date_picker)
        events_layout = QVBoxLayout()

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
            events_layout.addWidget(frame)

        scroll_content = QWidget()
        scroll_content.setLayout(events_layout)

        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("background: transparent; border: none;")
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_content)
        
        main_layout.addWidget(scroll_area)