


from PySide6.QtWidgets import *                                         
from PySide6.QtCore import *                               
from PySide6.QtGui import *      
from PySide6.QtUiTools import *


class Freeze_TableWidget(QTableView):
    def __init__(self, model):
        super(Freeze_TableWidget, self).__init__()

        #self.fp_x = 2  # -
        #self.fp_y = 3  # |
        self.fp_x = 2  # -
        self.fp_y = 2  # |

        self.setModel(model)

        self.frozenCol_TableView = QTableView(self)
        self.frozenRow_TableView = QTableView(self)
        self.corner_TableView = QTableView(self)

        self.init()

        for x in range(self.fp_x):
            self.horizontalHeader().setSectionResizeMode(x, QHeaderView.Fixed)
        for y in range(self.fp_y):
            self.verticalHeader().setSectionResizeMode(y, QHeaderView.Fixed)

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
        #        QHeaderView.Fixed)
                QHeaderView.Interactive)
        self.frozenCol_TableView.horizontalHeader().sectionResized.connect(self.FrozenColUpdateSectionWidth)

        #self.viewport().stackUnder(self.frozenCol_TableView)

        self.frozenCol_TableView.setStyleSheet('''
            QTableView { border: none;
                         background-color: none;
                         selection-background-color: #999;
                         border-right: 2px solid green;
            }''') # for demo purposes

        self.frozenCol_TableView.setSelectionModel(self.selectionModel())
        #for col in range(1, self.model().columnCount()):
        for col in range(self.fp_x, self.model().columnCount()):
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
        #        QHeaderView.Fixed)
                QHeaderView.Interactive)
        self.frozenRow_TableView.verticalHeader().sectionResized.connect(self.FrozenRowUpdateSectionHeight)

        self.frozenRow_TableView.setStyleSheet('''
            QTableView { border: none;
                         background-color: none;
                         selection-background-color: #999;
                         border-bottom: 2px solid green;
            }''') # for demo purposes

        self.frozenRow_TableView.setSelectionModel(self.selectionModel())
        #for row in range(1, self.model().rowCount()):
        for row in range(self.fp_y, self.model().rowCount()):
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
        self.corner_TableView.verticalHeader().hide()
        #self.corner_TableView.horizontalHeader().setSectionResizeMode(
        #        QHeaderView.Fixed)
        #self.corner_TableView.verticalHeader().setSectionResizeMode(
        #        QHeaderView.Fixed)

        #self.conner_TableView.verticalHeader().sectionResized.connect(self.ConnerUpdateSectionHeight)
        self.corner_TableView.setStyleSheet('''
            QTableView { border: none;
                         background-color: none;
                         selection-background-color: #999;
                         border-bottom: 2px solid green;
                         border-right: 2px solid green;
            }''') # for demo purposes

        self.corner_TableView.setSelectionModel(self.selectionModel())
        for row in range(self.fp_y, self.model().rowCount()):
            self.corner_TableView.setRowHidden(row, True)
        for col in range(self.fp_x, self.model().columnCount()):
            self.corner_TableView.setColumnHidden(col, True)
        self.corner_TableView.verticalHeader().setFixedWidth(self.verticalHeader().width())
        self.corner_TableView.setRowHeight(0, self.rowHeight(0))
        self.corner_TableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.corner_TableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


        #self.viewport().stackUnder(self.corner_TableView)
        #self.corner_TableView.viewport().stackUnder(self.frozenCol_TableView)
        #self.corner_TableView.viewport().stackUnder(self.frozenRow_TableView)
        self.corner_TableView.show()

        self.updateFrozenTableGeometry()
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.frozenCol_TableView.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        ###
        self.frozenRow_TableView.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.setStyleSheet('''
            QTableView { border: none;
                         background-color: none ;
                         selection-background-color: #999;
            }''') # for demo purposes


    def updateSectionWidth(self, logicalIndex, oldSize, newSize):
        #print("Base Width", logicalIndex)
        self.frozenRow_TableView.setColumnWidth(logicalIndex, newSize)
        #if logicalIndex == 0:
        #    self.frozenCol_TableView.setColumnWidth(0, newSize)
        #    self.corner_TableView.setColumnWidth(0, newSize)
        #    self.updateFrozenTableGeometry()

        #if logicalIndex == self.fp_x - 1:
        #     print("Col boundary")


    def updateSectionHeight(self, logicalIndex, oldSize, newSize):
        #print("Base Hight", logicalIndex)
        self.frozenCol_TableView.setRowHeight(logicalIndex, newSize)
        #if logicalIndex == 0:
        #    self.frozenRow_TableView.setRowHeight(logicalIndex, newSize)
        #    self.corner_TableView.setRowHeight(logicalIndex, newSize)
        #    self.updateFrozenTableGeometry()

        #if logicalIndex == self.fp_y - 1:
        #     print("Row boundary")

    #def CornerUpdateSectionWidth(self, logicalIndex, oldSize, newSize):
    #    print("Conner Width", logicalIndex)


    #def CornerUpdateSectionHeight(self, logicalIndex, oldSize, newSize):
    #    print("Corner Hight", logicalIndex)

    def FrozenColUpdateSectionWidth(self, logicalIndex, oldSize, newSize):
        #print("FrozenCol Width", logicalIndex)
        self.corner_TableView.setColumnWidth(logicalIndex, newSize)
        if logicalIndex < self.fp_x:
          #print("   set setColumnWidth", oldSize, newSize)
          #self.setColumnWidth(logicalIndex + 1, newSize)
          self.setColumnWidth(logicalIndex , newSize)
        if logicalIndex < self.fp_x:
          s = newSize- oldSize
          r = self.frozenCol_TableView.rect()
          self.frozenCol_TableView.setGeometry(self.verticalHeader().width(), r.y()+ self.frameWidth() , r.width() + s, r.height())
          r = self.corner_TableView.rect()
          self.corner_TableView.setGeometry(self.verticalHeader().width(), self.horizontalHeader().height() , r.width() + s, r.height())
        pass
        #if logicalIndex == self.fp_x :
        #     print("Frozen Col boundary")

    def FrozenRowUpdateSectionHeight(self, logicalIndex, oldSize, newSize):
        #print("FrozenRow Height",logicalIndex)
        self.corner_TableView.setRowHeight(logicalIndex, newSize)
        if logicalIndex < self.fp_y :
          #self.setRowHeight(logicalIndex + 1, newSize)
          self.setRowHeight(logicalIndex , newSize)
          s = newSize- oldSize
          r = self.frozenRow_TableView.rect()
          self.frozenRow_TableView.setGeometry(self.frameWidth(), self.horizontalHeader().height() , r.width() , r.height() + s)
          r = self.corner_TableView.rect()
          self.corner_TableView.setGeometry(self.verticalHeader().width(), self.horizontalHeader().height() , r.width() , r.height()+ s)
        #if logicalIndex == self.fp_y :
        #     print("Frozen Row boundary")

    def ConnerUpdateSectionHeight(self, logicalIndex, oldSize, newSize):
        #print("Conner Height")
        pass

    def resizeEvent(self, event):
        super(Freeze_TableWidget, self).resizeEvent(event)
        self.updateFrozenTableGeometry()

    def moveCursor_(self, cursorAction, modifiers):
        current = super(Freeze_TableWidget, self).moveCursor(cursorAction, modifiers)
        return current

    def moveCursor_2(self, cursorAction, modifiers):
        current = super(Freeze_TableWidget, self).moveCursor(cursorAction, modifiers)
        if (cursorAction == self.MoveLeft and
                self.visualRect(current).topLeft().x() <
                    self.frozenCol_TableView.columnWidth(0)):
            newValue = (self.horizontalScrollBar().value() +
                        self.visualRect(current).topLeft().x() -
                        self.frozenCol_TableView.columnWidth(0))
            self.horizontalScrollBar().setValue(newValue)
        return current

    def moveCursor(self, cursorAction, modifiers):
        current = super(Freeze_TableWidget, self).moveCursor(cursorAction, modifiers)

        total_width = 0
        for i in range(self.fp_x ):
               total_width += self.columnWidth(i)

        total_height = 0
        for i in range(self.fp_y ):
               total_height += self.rowHeight(i)

        if (cursorAction == QAbstractItemView.MoveLeft and
                self.visualRect(current).topLeft().x() <
                    total_width ):
            newValue = (self.horizontalScrollBar().value() +
                        self.visualRect(current).topLeft().x() -
                        total_width)
            self.horizontalScrollBar().setValue(newValue)

        if (cursorAction == QAbstractItemView.MoveUp and
                self.visualRect(current).topLeft().y() <
                    total_height ):
            newValue = (self.verticalScrollBar().value() +
                        self.visualRect(current).topLeft().y() -
                        total_height)
            self.verticalScrollBar().setValue(newValue)
        return current

    def scrollTo(self, index, hint):
        if index.column() > 0:
            super(Freeze_TableWidget, self).scrollTo(index, hint)

    def updateFrozenTableGeometry(self):
        total_width = 0
        for i in range(self.fp_x ):
               total_width += self.columnWidth(i)
        self.frozenCol_TableView.setGeometry(
                self.verticalHeader().width() ,
                self.frameWidth(), 
                #self.columnWidth(0),
                total_width,
                self.viewport().height() + self.horizontalHeader().height()
                )

        total_height = 0
        for i in range(self.fp_y ):
               total_height += self.rowHeight(i)
        self.frozenRow_TableView.setGeometry(
                self.frameWidth() , 
                #0,
                #self.horizontalHeader().height() + self.frameWidth(),
                self.horizontalHeader().height() ,
                self.viewport().width() + self.verticalHeader().width(),
                #self.rowHeight(0)
                total_height
                )

        self.corner_TableView.setGeometry(
                #self.frameWidth(), 
                #self.frameWidth() + self.verticalHeader().width(), 
                self.verticalHeader().width(), 
                self.horizontalHeader().height() ,
                #self.verticalHeader().width() + self.columnWidth(0),
                #self.verticalHeader().width() + total_width,
                total_width,
                #self.rowHeight(0)
                total_height
                )


def main(args):
    def split_and_strip(s, splitter):
        return [s.strip() for s in line.split(splitter)]

    app = QApplication(args)
    model = QStandardItemModel()
    #file = QFile(QFileInfo(__file__).absolutePath() + '/grades.txt')
    #file = QFile(QFileInfo(__file__).absolutePath() + '/customers-100.csv')
    #file = QFile(QFileInfo(__file__).absolutePath() + '/people-1000.csv')
    file = QFile(QFileInfo(__file__).absolutePath() + '/sample_csv.csv')
    if file.open(QFile.ReadOnly):
        #line = file.readLine(200).decode('utf-8')
        #line = str (file.readLine(200), 'utf-8')
        line = str (file.readLine(), 'utf-8')
        header = split_and_strip(line, ',')
        model.setHorizontalHeaderLabels(header)
        row = 0
        #while file.canReadLine():
        while not file.atEnd():
            #line = file.readLine(200).decode('utf-8')
            #line = str(file.readLine(200),'utf-8')
            line = str(file.readLine(),'utf-8')
            if not line.startswith('#') and ',' in line:
                fields = split_and_strip(line, ',')
                for col, field in enumerate(fields):
                    newItem = QStandardItem(field)
                    model.setItem(row, col, newItem)
                row += 1
                #print(row)
                #print(line)
    file.close()
    tableView = Freeze_TableWidget(model)
    tableView.setWindowTitle("Frozen Column Example")
    tableView.resize(860, 680)
    #tableView.resize(560, 380)
    tableView.show()
    return app.exec()


if __name__ == '__main__':
    import sys
    main(sys.argv)
