from PySide6.QtWidgets import (QTreeWidget, QTreeWidgetItem, QAbstractItemView)


from PySide6.QtWidgets import QApplication

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

    widget.show()
    app.exec()

