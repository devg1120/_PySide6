#from PySide import QtCore, QtGui
from PySide6.QtWidgets import *                                         
from PySide6.QtCore import *                               
from PySide6.QtGui import *                 
from PySide6.QtUiTools import *

import sys, os

class DragAndDrop(QLabel):
    def __init__(self):
        super().__init__()
        self.setText('Drag and drop here')
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        filename = os.path.basename(event.mimeData().urls()[0].path())
        self.setText(filename)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = DragAndDrop()
    w.show()
    sys.exit(app.exec_())

