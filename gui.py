import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class Book:
    
    def __init__(self, path=""):
        file = open(path,encoding="utf8")
        lines = file.readlines()
        
        self.text = lines[::2]
        
        
class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


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
        
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        main = QtWidgets.QWidget()
        
        # setting geometry
        self.setGeometry(100, 100, 600, 400)

        self.main_layout = QtWidgets.QVBoxLayout(main)
        
        # calling method
        self.min_amount = 1
        self.textBar()
        self.inputBox()

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        
        self.main_layout.addWidget(sc)
    
        self.setCentralWidget(main)

        self.show()
        
    def on_int_changed(self,text):
        print(text)
        if len(text) >= 1:
            self.min_amount = int(text)
            self.updateTextBar()
        
    def inputBox(self):
        inputBox = QtWidgets.QWidget()
        
        layout = QtWidgets.QFormLayout()
        
        self.int_line_edit = QtWidgets.QLineEdit(parent=self)
        self.int_line_edit.setText("1")
        self.int_line_edit.setValidator(QtGui.QIntValidator())
        
        self.int_line_edit.textChanged.connect(self.on_int_changed)
        
        layout.addRow("Minimum Number of Words:",  self.int_line_edit)
        inputBox.setLayout(layout)
        
        self.main_layout.addWidget(inputBox)
        
    def updateTextBar(self):
        
        raw_text = []
        
        for line in self.book.text:
            if len(line.split()) >= self.min_amount:
                raw_text.append(line)
                
        
        text = ""
        for item in raw_text:
            text = text + item + "\n"
            
        
        self.text_area.setText(text)

        
    # method for widgets
    def textBar(self):
        # text to show in label
        self.book = Book("books/HarryPotter/01_Sorcerers_Stone.txt")
        raw_text = []
        
        for line in self.book.text:
            if len(line.split()) >= self.min_amount:
                raw_text.append(line)
        
        text = ""
        for item in raw_text:
            text = text + item + "\n"
            
        # creating scroll label
        self.text_area = ScrollLabel(self)

        # setting text to the label
        self.text_area.setText(text)

        # setting geometry
        self.text_area.setGeometry(100, 100, 200, 80)
        
        self.main_layout.addWidget(self.text_area)


# create pyqt5 app

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()