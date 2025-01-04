import sys, enum
#from PySide import QtCore, QtGui

from PySide6.QtWidgets import *                                         
from PySide6.QtCore import *                               
from PySide6.QtGui import *                 
from PySide6.QtUiTools import *

class Item(QLabel):
    Manipilate = enum.Enum('Manipilate', 'none move resize_l resize_r')
    
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet('background-color: white; border: 1px solid black; padding: 4px;')
        self.resize(128, 64)
        self._mani = Item.Manipilate.none
        self._offset = QPoint(0, 0)
        self._rect = self.rect()
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        pos = event.pos()
        if self._mani == Item.Manipilate.none:
            self._mani = self.get_manipulation(pos)
        self._offset = event.pos()
        self._rect = self.geometry()

    def mouseReleaseEvent(self, event):
        self._mani = Item.Manipilate.none

    def mouseMoveEvent(self, event):
        pos = event.pos()
        if self._mani == Item.Manipilate.none:
            self.setCursor({
                Item.Manipilate.none: Qt.ArrowCursor,
                Item.Manipilate.move: Qt.ArrowCursor,
                Item.Manipilate.resize_l: Qt.SizeHorCursor,
                Item.Manipilate.resize_r: Qt.SizeHorCursor
            }[self.get_manipulation(pos)])
        elif self._mani == Item.Manipilate.move:
            self.move(self.mapToParent(pos - self._offset))
        elif self._mani == Item.Manipilate.resize_l:
            sub = pos - self._offset
            self.setGeometry(self._rect.x() + sub.x(), self._rect.y(), self._rect.width() - sub.x(), self._rect.height())
            self._rect = self.geometry()
        elif self._mani == Item.Manipilate.resize_r:
            sub = pos - self._offset
            self.setGeometry(self._rect.x(), self._rect.y(), self._rect.width() + sub.x(), self._rect.height())
        self.update()

    def get_manipulation(self, pos):
        if pos.x() < 8:
            return Item.Manipilate.resize_l
        if pos.x() > (self.width() - 8):
            return Item.Manipilate.resize_r
        else:
            return Item.Manipilate.move

app = QApplication(sys.argv)
widget = QWidget()
widget.setFixedSize(640, 480)
item = Item('item')
item.setStyleSheet("QLabel { background-color:red  ; }")



item.setParent(widget)
item.move(0, 0)
widget.show()
sys.exit(app.exec())

