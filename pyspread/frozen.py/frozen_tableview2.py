

#from PyQt5.QtCore import QFile, QFileInfo, Qt
#from PyQt5.QtGui import QStandardItem, QStandardItemModel
#from PyQt5.QtWidgets import QApplication, QHeaderView, QTableView

from PySide6.QtWidgets import *                                         
from PySide6.QtCore import *                               
from PySide6.QtGui import *      
from PySide6.QtUiTools import *


class Freeze_TableWidget(QTableView):
    def __init__(self, model):
        super(Freeze_TableWidget, self).__init__()
        self.setModel(model)

        self.frozenCol_TableView = QTableView(self)
        self.frozenRow_TableView = QTableView(self)
        self.corner_TableView = QTableView(self)

        self.init()
        self.horizontalHeader().sectionResized.connect(self.updateSectionWidth)
        self.verticalHeader().sectionResized.connect(self.updateSectionHeight)

        self.frozenCol_TableView.verticalScrollBar().valueChanged.connect(
            self.verticalScrollBar().setValue)
        self.verticalScrollBar().valueChanged.connect(
            self.frozenCol_TableView.verticalScrollBar().setValue)

        self.frozenRow_TableView.horizontalScrollBar().valueChanged.connect(
            self.horizontalScrollBar().setValue)
        self.horizontalScrollBar().valueChanged.connect(
            self.frozenRow_TableView.horizontalScrollBar().setValue)


    def init(self):
        self.frozenCol_TableView.setModel(self.model())
        self.frozenCol_TableView.setFocusPolicy(Qt.NoFocus)
        self.frozenCol_TableView.verticalHeader().hide()
        self.frozenCol_TableView.horizontalHeader().setSectionResizeMode(
                QHeaderView.Fixed)
        #self.viewport().stackUnder(self.frozenCol_TableView)

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

        ####
        self.frozenRow_TableView.setModel(self.model())
        self.frozenRow_TableView.setFocusPolicy(Qt.NoFocus)
        self.frozenRow_TableView.horizontalHeader().hide()
        self.frozenRow_TableView.verticalHeader().setSectionResizeMode(
                QHeaderView.Fixed)

        self.frozenRow_TableView.setStyleSheet('''
            QTableView { border: none;
                         background-color: #ffffff;
                         selection-background-color: #999;
                         border-bottom: 2px solid green;
            }''') # for demo purposes

        self.frozenRow_TableView.setSelectionModel(self.selectionModel())
        for row in range(1, self.model().rowCount()):
            self.frozenRow_TableView.setRowHidden(row, True)
        self.frozenRow_TableView.verticalHeader().setFixedWidth(self.verticalHeader().width())
        self.frozenRow_TableView.setRowHeight(0, self.rowHeight(0))
        self.frozenRow_TableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozenRow_TableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozenRow_TableView.show()

        ####
        self.corner_TableView.setModel(self.model())
        self.corner_TableView.setFocusPolicy(Qt.NoFocus)
        self.corner_TableView.horizontalHeader().hide()
        self.corner_TableView.verticalHeader().setSectionResizeMode(
                QHeaderView.Fixed)

        self.corner_TableView.setStyleSheet('''
            QTableView { border: none;
                         background-color: yellow;
                         selection-background-color: #999;
                         border-bottom: 2px solid green;
                         border-right: 2px solid green;
            }''') # for demo purposes

        self.corner_TableView.setSelectionModel(self.selectionModel())
        for row in range(1, self.model().rowCount()):
            self.corner_TableView.setRowHidden(row, True)
        for col in range(1, self.model().columnCount()):
            self.corner_TableView.setColumnHidden(col, True)
        self.corner_TableView.verticalHeader().setFixedWidth(self.verticalHeader().width())
        self.corner_TableView.setRowHeight(0, self.rowHeight(0))
        self.corner_TableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.corner_TableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.corner_TableView.show()


        self.updateFrozenTableGeometry()
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.frozenCol_TableView.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        ###
        self.frozenRow_TableView.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)



    def updateSectionWidth(self, logicalIndex, oldSize, newSize):
        #if self.logicalIndex == 0:
        if logicalIndex == 0:
            self.frozenCol_TableView.setColumnWidth(0, newSize)
            self.corner_TableView.setColumnWidth(0, newSize)
            self.updateFrozenTableGeometry()
        ###
        self.frozenRow_TableView.setColumnWidth(logicalIndex, newSize)

    def updateSectionHeight(self, logicalIndex, oldSize, newSize):
        self.frozenCol_TableView.setRowHeight(logicalIndex, newSize)
        ###
        if logicalIndex == 0:
            print("set", newSize)
            self.frozenRow_TableView.setRowHeight(logicalIndex, newSize)
            self.corner_TableView.setRowHeight(logicalIndex, newSize)
            self.updateFrozenTableGeometry()

    def resizeEvent(self, event):
        super(Freeze_TableWidget, self).resizeEvent(event)
        self.updateFrozenTableGeometry()

    def moveCursor_(self, cursorAction, modifiers):
        current = super(Freeze_TableWidget, self).moveCursor(cursorAction, modifiers)
        return current

    def moveCursor(self, cursorAction, modifiers):
        current = super(Freeze_TableWidget, self).moveCursor(cursorAction, modifiers)
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
            super(Freeze_TableWidget, self).scrollTo(index, hint)

    def updateFrozenTableGeometry(self):
        self.frozenCol_TableView.setGeometry(
                self.verticalHeader().width() + self.frameWidth(),
                self.frameWidth(), 
                self.columnWidth(0),
                self.viewport().height() + self.horizontalHeader().height())

        self.frozenRow_TableView.setGeometry(
                #self.verticalHeader().width() + self.frameWidth() , 
                self.frameWidth(), 
                self.horizontalHeader().height() + self.frameWidth(),
                self.viewport().width() + self.verticalHeader().width(),
                self.rowHeight(0))

        self.corner_TableView.setGeometry(
                self.frameWidth(), 
                self.horizontalHeader().height() + self.frameWidth(),
                #self.viewport().width() + self.verticalHeader().width(),
                self.verticalHeader().width() + self.columnWidth(0),
                self.rowHeight(0))


def main(args):
    def split_and_strip(s, splitter):
        return [s.strip() for s in line.split(splitter)]

    app = QApplication(args)
    model = QStandardItemModel()
    #file = QFile(QFileInfo(__file__).absolutePath() + '/grades.txt')
    file = QFile(QFileInfo(__file__).absolutePath() + '/people-1000.csv')

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
    tableView = Freeze_TableWidget(model)
    tableView.setWindowTitle("Frozen Column Example")
    #tableView.resize(560, 680)
    tableView.resize(560, 380)
    tableView.show()
    return app.exec()


if __name__ == '__main__':
    import sys
    main(sys.argv)
