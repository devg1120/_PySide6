

#from PyQt5.QtCore import QFile, QFileInfo, Qt
#from PyQt5.QtGui import QStandardItem, QStandardItemModel
#from PyQt5.QtWidgets import QApplication, QHeaderView, QTableView

from PySide6.QtWidgets import *                                         
from PySide6.QtCore import *                               
from PySide6.QtGui import *      
from PySide6.QtUiTools import *



class FreezeRow_TableWidget(QTableView):
    def __init__(self, model):
        super(FreezeRow_TableWidget, self).__init__()
        self.setModel(model)
        self.frozenRow_TableView = QTableView(self)
        self.init()
        self.horizontalHeader().sectionResized.connect(self.updateSectionWidth)
        self.verticalHeader().sectionResized.connect(self.updateSectionHeight)

        #self.frozenRow_TableView.verticalScrollBar().valueChanged.connect(
        #    self.verticalScrollBar().setValue)
        #self.verticalScrollBar().valueChanged.connect(
        #    self.frozenRow_TableView.verticalScrollBar().setValue)
        self.frozenRow_TableView.horizontalScrollBar().valueChanged.connect(
            self.horizontalScrollBar().setValue)
        self.horizontalScrollBar().valueChanged.connect(
            self.frozenRow_TableView.horizontalScrollBar().setValue)

    def init(self):
        self.frozenRow_TableView.setModel(self.model())
        self.frozenRow_TableView.setFocusPolicy(Qt.NoFocus)
        #self.frozenRow_TableView.verticalHeader().hide()
        self.frozenRow_TableView.horizontalHeader().hide()
        #self.frozenRow_TableView.horizontalHeader().setSectionResizeMode(
        self.frozenRow_TableView.verticalHeader().setSectionResizeMode(
                QHeaderView.Fixed)
        self.viewport().stackUnder(self.frozenRow_TableView)

        self.frozenRow_TableView.setStyleSheet('''
            QTableView { border: none;
                         background-color: #ffffff;
                         selection-background-color: #999;
                         border-bottom: 2px solid green;
            }''') # for demo purposes

        self.frozenRow_TableView.setSelectionModel(self.selectionModel())
        #for col in range(1, self.model().columnCount()):
        #    self.frozenRow_TableView.setColumnHidden(col, True)
        for row in range(1, self.model().rowCount()):
            self.frozenRow_TableView.setRowHidden(row, True)
        self.frozenRow_TableView.verticalHeader().setFixedWidth(self.verticalHeader().width())
        #self.frozenRow_TableView.setColumnWidth(0, self.columnWidth(0))
        self.frozenRow_TableView.setRowHeight(0, self.rowHeight(0))
        self.frozenRow_TableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozenRow_TableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozenRow_TableView.show()
        self.updateFrozenTableGeometry()
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        #self.frozenRow_TableView.setVerticalScrollMode(self.ScrollPerPixel)
        self.frozenRow_TableView.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

    def updateSectionWidth(self, logicalIndex, oldSize, newSize):
        print("updateSectionWidth:", logicalIndex)
        self.frozenRow_TableView.setColumnWidth(logicalIndex, newSize)
        pass
        #if self.logicalIndex == 0:
        #    self.frozenRow_TableView.setColumnWidth(0, newSize)
        #    self.updateFrozenTableGeometry()

    def updateSectionHeight(self, logicalIndex, oldSize, newSize):
        print("updateSectionHeight:", logicalIndex)
        if logicalIndex == 0:
            print("set", newSize)
            self.frozenRow_TableView.setRowHeight(logicalIndex, newSize)
            self.updateFrozenTableGeometry()

    def resizeEvent(self, event):
        super(FreezeRow_TableWidget, self).resizeEvent(event)
        self.updateFrozenTableGeometry()

    def moveCursor__(self, cursorAction, modifiers):
        current = super(FreezeRow_TableWidget, self).moveCursor(cursorAction, modifiers)
        return current

    def moveCursor(self, cursorAction, modifiers):
        current = super(FreezeRow_TableWidget, self).moveCursor(cursorAction, modifiers)
        return current

    def moveCursor_(self, cursorAction, modifiers):
        current = super(FreezeRow_TableWidget, self).moveCursor(cursorAction, modifiers)
        if (cursorAction == self.MoveLeft or cursorAction == self.MoveRight ):
            pass
            #self.frozenRow_TableView.moveCursor(cursorAction, modifiers)
            #newValue = self.horizontalScrollBar().value() 
            #print(newValue)
            #self.frozenRow_TableView.horizontalScrollBar().setValue(newValue)
            #self.frozenRow_TableView.horizontalScrollBar().setValue(0)
        return current

    def moveCursor_(self, cursorAction, modifiers):
        current = super(FreezeRow_TableWidget, self).moveCursor(cursorAction, modifiers)
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
            super(FreezeRow_TableWidget, self).scrollTo(index, hint)

    #def updateFrozenTableGeometry(self):
    #    self.frozenRow_TableView.setGeometry(
    #            self.verticalHeader().width() + self.frameWidth(),
    #            self.frameWidth(), 
    #            self.columnWidth(0),
    #            self.viewport().height() + self.horizontalHeader().height())

    def updateFrozenTableGeometry(self):
        self.frozenRow_TableView.setGeometry(
                #self.verticalHeader().width() + self.frameWidth() , 
                self.frameWidth(), 
                self.horizontalHeader().height() + self.frameWidth(),
                self.viewport().width() + self.verticalHeader().width(),
                self.rowHeight(0))

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
    #tableView = FreezeCol_TableWidget(model)
    tableView = FreezeRow_TableWidget(model)
    tableView.setWindowTitle("Frozen Column Example")
    #tableView.resize(560, 680)
    tableView.resize(560, 380)
    tableView.show()
    return app.exec()


if __name__ == '__main__':
    import sys
    main(sys.argv)
