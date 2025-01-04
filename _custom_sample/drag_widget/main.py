import sys
#from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import *                                         
from PySide6.QtCore import *                               
from PySide6.QtGui import *                 
from PySide6.QtUiTools import *    


# ドラッグで動くWidget
class WidgetItem(QLabel):
    def __init__(self):
        super().__init__('')
        self.setStyleSheet('border: 1px solid black; background-color: red;')
        self.setFixedSize(32, 32)
        self._drag = False
        self._offset = QPoint(0, 0)

    def mousePressEvent(self, event):
        self._drag = True
        self._offset = event.pos()

    def mouseReleaseEvent(self, event):
        self._drag = False

    def mouseMoveEvent(self, event):
        if self._drag:
            self.move(self.mapToParent(event.pos() - self._offset))

app = QApplication(sys.argv)

widget = QWidget()
widget.setFixedSize(640, 480)
widget.setLayout(QVBoxLayout())
layout = widget.layout()
item = WidgetItem()
layout.addWidget(item)
widget.show()
sys.exit(app.exec_())
