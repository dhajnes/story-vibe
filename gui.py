import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sys

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
import torch
import requests
from bs4 import BeautifulSoup
import re

class Bert:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
        self.model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
        
    def process(self,text):
        tokens = self.tokenizer.encode(text, return_tensors='pt')
        # print(tokens)  # the embedded representation of the text
        result = self.model(tokens)
        return int(torch.argmax(result.logits))+1
    
class Book:
    
    def __init__(self, path=""):
        file = open(path,encoding="utf8")
        lines = file.readlines()
        
        self.text = np.array(lines[::2])
        
        self.lengths = np.zeros((len(self.text),1))
        
        for i,line in enumerate(self.text):
            self.lengths[i] = len(line.split())

    # class for scrollable label
class ScrollLabel(QtWidgets.QScrollArea):

    # constructor
    def __init__(self, *args, **kwargs):
        QtWidgets.QScrollArea.__init__(self, *args, **kwargs)

        # making widget resizable
        self.setWidgetResizable(True)

        # making qwidget object
        content = QtWidgets.QWidget(self)
        self.setWidget(content)

        # vertical box layout
        lay = QtWidgets.QVBoxLayout(content)

        # creating label
        self.label = QtWidgets.QLabel(content)

        # setting alignment to the text
        self.label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        # making label multi-line
        self.label.setWordWrap(True)

        # adding label to the layout
        lay.addWidget(self.label)

    # the setText method
    def setText(self, text):
        # setting text to the label
        self.label.setText(text)
        
class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)


class TextControl(QWidget):
    def __init__(self, main_window):
        super().__init__()  # "Image controls"
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Fixed)

        self.main_window = main_window

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet('background-color: lightgray; border-radius: 10px')
        # self.setFixedWidth(500)

        self.main_layout = QHBoxLayout()
        self.items = len(self.main_window.raw_text)
        
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(8, 0, 8, 0)
        button_layout.setSpacing(4)
        # button_layout.addStretch()

        back_button = QToolButton()
        back_button.setToolTip("Browse backward in list")
        back_button.setArrowType(QtCore.Qt.LeftArrow)
        back_button.setFixedSize(30, 30)
        back_button.clicked.connect(self.browse_backward)
        # back_button.setStyleSheet("border : 10px, border-color: beige;")
        button_layout.addWidget(back_button, 0,
                                QtCore.Qt.AlignmentFlag.AlignLeading |
                                QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.image_index = QLabel()
        self.image_index.setToolTip("Current selected image")
        self.image_index.setText("{} / {}".format(0, 0))
          
        button_layout.addWidget(self.image_index)

        forward_button = QToolButton()
        forward_button.setToolTip("Browse forward in list")
        forward_button.setArrowType(QtCore.Qt.RightArrow)
        forward_button.setFixedSize(30, 30)
        forward_button.clicked.connect(self.browse_forward)
        # forward_button.setStyleSheet("background-color: rgba(0,0,0,0);")
        button_layout.addWidget(forward_button, 0,
                                QtCore.Qt.AlignmentFlag.AlignLeading |
                                QtCore.Qt.AlignmentFlag.AlignVCenter)

        # button_layout.addStretch()
        self.main_layout.addStretch(10)
        self.main_layout.addLayout(button_layout)
        self.main_layout.addStretch(10)
        self.setLayout(self.main_layout)

    def updateText(self):
        self.items = len(self.main_window.raw_text)
        self.image_index.setText("{} / {}".format(self.main_window.raw_text_index, self.items-1))
    
    def browse_forward(self):
        
        index = self.main_window.raw_text_index
        
        if index == self.items-1:
            index = 0
        else:
            index += 1
            
        if len(self.main_window.raw_text) > 0:
            new_text = self.main_window.raw_text[index]
            self.main_window.text_area.setText(new_text)
        self.main_window.raw_text_index = index
        self.updateText()

    def browse_backward(self):
        index = self.main_window.raw_text_index
        
        if index == 0:
            index = self.items-1
        else:
            index -= 1
            
        if len(self.main_window.raw_text) > 0:
            new_text = self.main_window.raw_text[index]
            self.main_window.text_area.setText(new_text)
        self.main_window.raw_text_index = index
        self.updateText()
        
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.model = Bert()
        self.book = None
        
        self.raw_text_index = 0
        self.raw_text = []
        self.score_map = {}
        
        main = QWidget()
        
        # setting geometry
        self.setGeometry(100, 100, 600, 400)

        self.main_layout = QVBoxLayout(main)
        
        # calling method
        self.min_amount = 50
        self.createMenuBar()
        self.textBar()
        self.text_control = TextControl(self)
        self.main_layout.addWidget(self.text_control)
        
        self.inputBox()

        self.plot()
        
        self.score_label = QLabel()
        self.score_label.setText("Average Score for Book: ")
        
        self.main_layout.addWidget(self.score_label)
        
        self.setCentralWidget(main)

        self.show()
    
    def plot(self):
        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.sc.axes.plot()
        
        self.main_layout.addWidget(self.sc)
    
    def updatePlot(self):  
        self.sc.axes.cla() 
        x_axis = np.arange(len(self.raw_text))
        y_axis = []
        average_score = 0
        for line in self.raw_text:
            if line in self.score_map:
                value = self.score_map[line]
            else:
                value = self.model.process(line)
                self.score_map[line] = value
                
            y_axis.append(value)
            average_score += value
            
        if len(self.raw_text) != 0:
            average_score /= len(self.raw_text)
        else:
            average_score = ''
    
        self.score_label.setText("Average Score for Book: {}".format(average_score))
        
        self.sc.axes.plot(x_axis,y_axis)
        self.sc.fig.canvas.draw_idle()        
    
    def selectBook(self):        
        filter = "Text files (*.txt)"

        f = QFileDialog.getOpenFileName(directory="books/",filter=filter)
        if f[0] != '':
            self.book = Book(f[0])
            self.updateBook()
        
    def createMenuBar(self):
        menuBar = self.menuBar()
        # Creating menus using a QMenu object
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        self.openAction = QAction("Select Book",menuBar)
        self.openAction.triggered.connect(self.selectBook)
        fileMenu.addAction(self.openAction)
    
    def onIntChanged(self):
        text = self.int_line_edit.text()
        if len(text) >= 1:
            if self.min_amount != int(text):
                self.min_amount = int(text)
                self.updateBook()
                self.updateTextBar()
        
    def inputBox(self):
        inputBox = QWidget()
        
        layout = QFormLayout()
        
        self.int_line_edit = QLineEdit(parent=self)
        self.int_line_edit.setText("50")
        self.int_line_edit.setValidator(QtGui.QIntValidator())
        
        self.int_line_edit.editingFinished.connect(self.onIntChanged)
        
        layout.addRow("Minimum Number of Words:",  self.int_line_edit)
        inputBox.setLayout(layout)
        
        self.main_layout.addWidget(inputBox)
        
    def updateTextBar(self):
        
        self.raw_text_index = 0
        if len(self.raw_text) > 0:
            self.text_area.setText(self.raw_text[self.raw_text_index])

    def updateBook(self):
        if self.book == None:
            return
        
        # self.raw_text = []
        # for line in self.book.text:
        #     if len(line.split()) >= self.min_amount:
        #         self.raw_text.append(line)
                
        indicies = np.where(self.book.lengths >= self.min_amount)
        self.raw_text = self.book.text[indicies[0]]
        
        self.updateTextBar()
        self.updatePlot()
        self.text_control.updateText()
        
    # method for widgets
    def textBar(self):
        # text to show in label
            
        # creating scroll label
        self.text_area = ScrollLabel(self)
        self.main_layout.addWidget(self.text_area)


# create pyqt5 app

app = QApplication(sys.argv)
w = MainWindow()
app.exec_()

