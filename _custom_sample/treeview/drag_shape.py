import enum

from PySide6.QtWidgets import (QTreeWidget, QTreeWidgetItem, QAbstractItemView)


from PySide6.QtWidgets import QApplication
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *





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

class MyTreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super(MyTreeWidget, self).__init__(parent)
        self.setDragDropMode(QAbstractItemView.InternalMove)

    def dropEvent(self, event):
        source = event.source()
        pos = event.pos()
        destination_parent = source.itemAt(pos)

        if destination_parent is None:
            print("no parent")
            return

        if destination_parent.parent() is not None:
            print("destination is not top.")
            return

        print("move item")
        super(MyTreeWidget, self).dropEvent(event)


if __name__ == "__main__":
    #from SetupQt import setup_qt
    #from PySide6.QtWidgets import QApplication

    #setup_qt()  # for venv

    app = QApplication()
    widget = MyTreeWidget()

    top_level_items = []
    for i in range(3):
        item_p = QTreeWidgetItem()
        item_p.setText(0, "Data{0}".format(i))
        for j in range(2):
            item_c = QTreeWidgetItem(item_p)
            item_c.setText(0, "Data{0}{1}".format(i, j))
        top_level_items.append(item_p)

    widget.insertTopLevelItems(0, top_level_items)
    widget.expandAll()

    s = Item('item')
    s.setStyleSheet("QLabel { background-color:red  ; }")

    #s.setParent(widget)
    header = widget.headerItem()
    header.setBackground(0,QColor("blue"))

    row = widget.itemAt(13,43)
    row.setBackground(0,QColor("yellow"))
    #s.setParent(row.treeWidget())


    #item = widget.itemFromIndex(QModelIndex(2))
    #item.setBackground(0,QColor("blue"))

    #row = widget.takeTopLevelItem(0)
    #row = widget.topLevelItem(0)

    col = widget.itemWidget(row,0)
    print(col)
    #col.setStyleSheet("  background-color:red  ; ")

    #index = widget.indexFromItem(row,0)
    #item widget.itemFromIndex(item)
    #s.setParent(col)

    #s.setParent(widget)

    s.move(0, 0)


    widget.show()
    app.exec()

