#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
from PySide6.QtWidgets import *                                         
from PySide6.QtCore import *                               
from PySide6.QtGui import *      
from PySide6.QtUiTools import *

import sys
import time
 

class MyWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
       
        self.tableWidget1 = QTableWidget()
        self.tableWidget2 = QTableWidget()
        numRows = 40
        numCols = 2
        self.tableWidget1.setRowCount(numRows)
        self.tableWidget1.setColumnCount(numCols)
        self.tableWidget2.setRowCount(numRows)
        self.tableWidget2.setColumnCount(numCols)
       
        layout = QHBoxLayout(self)
        layout.addWidget(self.tableWidget1)
        layout.addWidget(self.tableWidget2)

        self.setLayout(layout)

        self.sliderBar1 = self.tableWidget1.verticalScrollBar()
        self.sliderBar2 = self.tableWidget2.verticalScrollBar()

        QObject.connect(self.sliderBar1, 
                               SIGNAL("actionTriggered(int)"),
self.SyncScroll)
       
    def SyncScroll(self):
        sliderValue = self.sliderBar1.value()
        self.sliderBar2.setValue(sliderValue)



def main():
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 
