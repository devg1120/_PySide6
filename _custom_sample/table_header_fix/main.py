import sys
#from PySide import QtGui
from PySide6.QtWidgets import *                                         
from PySide6.QtCore import *                               
from PySide6.QtGui import *                 
from PySide6.QtUiTools import *  

class MyTable(QWidget):
    def __init__(self):
        super().__init__()
        lo = QHBoxLayout()
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(0)
        self.setLayout(lo)

        self._header = QLabel('header')
        self._header.setStyleSheet('border-right: 1px solid black;\
            border-bottom: 1px solid black;\
            background-color: red;')
        self._header.setFixedSize(128, 32)
        lo.addWidget(self._header)

        for i in range(0, 8):
            item = QLabel('cell {0}'.format(i))
            item.setStyleSheet('border-right: 1px solid black;\
                border-bottom: 1px solid black;\
                background-color: white;')
            item.setFixedSize(128, 32)
            lo.addWidget(item)

    def setHeaderPos(self, x, y):
        self._header.move(x, y)
        self._header.raise_()


app = QApplication(sys.argv)
table = MyTable()
scroll = QScrollArea()
scroll.setWidget(table)

def moveHeader():
    x = scroll.horizontalScrollBar().value()
    table.setHeaderPos(x, 0)

scroll.horizontalScrollBar().valueChanged.connect(moveHeader)
scroll.show()
sys.exit(app.exec_())

