

#from PyQt5.QtCore import QFile, QFileInfo, Qt
#from PyQt5.QtGui import QStandardItem, QStandardItemModel
#from PyQt5.QtWidgets import QApplication, QHeaderView, QTableView

from PySide6.QtWidgets import *                                         
from PySide6.QtCore import *                               
from PySide6.QtGui import *      
from PySide6.QtUiTools import *


class FreezeCol_TableWidget(QTableView):
    def __init__(self, model):
        super(FreezeCol_TableWidget, self).__init__()
        self.setModel(model)
        self.frozenCol_TableView = QTableView(self)
        self.init()
        self.horizontalHeader().sectionResized.connect(self.updateSectionWidth)
        self.verticalHeader().sectionResized.connect(self.updateSectionHeight)
        self.frozenCol_TableView.verticalScrollBar().valueChanged.connect(
            self.verticalScrollBar().setValue)
        self.verticalScrollBar().valueChanged.connect(
            self.frozenCol_TableView.verticalScrollBar().setValue)

    def init(self):
        self.frozenCol_TableView.setModel(self.model())
        self.frozenCol_TableView.setFocusPolicy(Qt.NoFocus)
        self.frozenCol_TableView.verticalHeader().hide()
        self.frozenCol_TableView.horizontalHeader().setSectionResizeMode(
                QHeaderView.Fixed)
        self.viewport().stackUnder(self.frozenCol_TableView)

        #self.frozenCol_TableView.setStyleSheet('''
        #    QTableView { border: none;
        #                 background-color: #8EDE21;
        #                 selection-background-color: #999;
        #    }''') # for demo purposes

        self.frozenCol_TableView.setStyleSheet('''
            QTableView { border: none;
                         background-color: #ffffff;
                         selection-background-color: #999;
                         border-right: 2px solid green;
            }''') # for demo purposes
        self.frozenCol_TableView.setSelectionModel(self.selectionModel())
        for col in range(1, self.model().columnCount()):
            self.frozenCol_TableView.setColumnHidden(col, True)
        self.frozenCol_TableView.setColumnWidth(0, self.columnWidth(0))
        self.frozenCol_TableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozenCol_TableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozenCol_TableView.show()
        self.updateFrozenTableGeometry()
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.frozenCol_TableView.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

    def updateSectionWidth(self, logicalIndex, oldSize, newSize):
        #if self.logicalIndex == 0:
        if logicalIndex == 0:
            self.frozenCol_TableView.setColumnWidth(0, newSize)
            self.updateFrozenTableGeometry()

    def updateSectionHeight(self, logicalIndex, oldSize, newSize):
        self.frozenCol_TableView.setRowHeight(logicalIndex, newSize)

    def resizeEvent(self, event):
        super(FreezeCol_TableWidget, self).resizeEvent(event)
        self.updateFrozenTableGeometry()

    def moveCursor(self, cursorAction, modifiers):
        current = super(FreezeCol_TableWidget, self).moveCursor(cursorAction, modifiers)
        #if (cursorAction == self.MoveLeft and
        #        self.current.column() > 0 and
        if (cursorAction == self.MoveLeft and
                self.visualRect(current).topLeft().x() <
                    self.frozenCol_TableView.columnWidth(0)):
            newValue = (self.horizontalScrollBar().value() +
                        self.visualRect(current).topLeft().x() -
                        self.frozenCol_TableView.columnWidth(0))
            self.horizontalScrollBar().setValue(newValue)
        return current

    def scrollTo(self, index, hint):
        if index.column() > 0:
            super(FreezeCol_TableWidget, self).scrollTo(index, hint)

    def updateFrozenTableGeometry(self):
        self.frozenCol_TableView.setGeometry(
                self.verticalHeader().width() + self.frameWidth(),
                self.frameWidth(), 
                self.columnWidth(0),
                self.viewport().height() + self.horizontalHeader().height())


def main(args):
    def split_and_strip(s, splitter):
        return [s.strip() for s in line.split(splitter)]

    app = QApplication(args)
    model = QStandardItemModel()
    file = QFile(QFileInfo(__file__).absolutePath() + '/grades.txt')
    if file.open(QFile.ReadOnly):
        #line = file.readLine(200).decode('utf-8')
        line = str (file.readLine(200), 'utf-8')
        header = split_and_strip(line, ',')
        model.setHorizontalHeaderLabels(header)
        row = 0
        while file.canReadLine():
            #line = file.readLine(200).decode('utf-8')
            line = str(file.readLine(200),'utf-8')
            if not line.startswith('#') and ',' in line:
                fields = split_and_strip(line, ',')
                for col, field in enumerate(fields):
                    newItem = QStandardItem(field)
                    model.setItem(row, col, newItem)
                row += 1
    file.close()
    tableView = FreezeCol_TableWidget(model)
    tableView.setWindowTitle("Frozen Column Example")
    #tableView.resize(560, 680)
    tableView.resize(560, 380)
    tableView.show()
    return app.exec()


if __name__ == '__main__':
    import sys
    main(sys.argv)
