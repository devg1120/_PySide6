import enum
import sys

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


class WorkSheet(QTableWidget):
    def __init__(self, row_max=256, col_max=100):
        super().__init__(row_max, col_max)
        self.setStyleSheet("""
            QTableWidget {
                font-family: monospace;
            }
            QTableCornerButton::section {
                background: #fff;
            }
            QHeaderView {
                font-family: monospace;
                background: #eee;
                color: #666;
            }
        """)
        self.itemChanged.connect(self.cell_updated)

        header_horiz = QHeaderView(Qt.Orientation.Horizontal, parent=self)
        header_horiz.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.setHorizontalHeader(header_horiz)

        header_vert = QHeaderView(Qt.Orientation.Vertical, parent=self)
        header_vert.setDefaultAlignment(Qt.AlignmentFlag.AlignRight)
        header_vert.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.setVerticalHeader(header_vert)

    def cell_updated(self, item: QTableWidgetItem):
        value = item.text()
        if self.is_num(value):
            item.setText(str(float(value)))
            item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
        else:
            item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)

    @staticmethod
    def is_num(str_float: str) -> bool:
        try:
            float(str_float)
        except ValueError:
            return False
        else:
            return True


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('WorkSheet test')
        self.resize(800, 600)
        self.init_ui()

    def init_ui(self):
        sheet = WorkSheet()
        self.setCentralWidget(sheet)


def main():
    """Main event loop
    """
    app = QApplication(sys.argv)
    obj = Example()

    s = Item('item')
    s.setStyleSheet("QLabel { background-color:red  ; }")
    s.setParent(obj)
    s.move(0, 0)

    obj.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()


"""
    s = Item('item')
    s.setStyleSheet("QLabel { background-color:red  ; }")

    s.setParent(widget)

    s.move(0, 0)


    widget.show()
    app.exec()

"""
