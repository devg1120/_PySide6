"""シグナル&スロットを使用して MVVM 的な動作をさせる実験.
Model → ViewModel → View の通信はシグナルで間接的に行われます。
Model は ViewModel のことを一切知らず、ViewModel は View のことを一切知りません。
Model のシグナルを受け取れるのであれば、ViewModel や View を全く別のものに置き換えることもできます。
"""
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget, QApplication, QLineEdit, QVBoxLayout

class Model(QObject):
    """表示に依存しないデータ/ロジッククラス.
    :param parent: 親オブジェクト
    """
    # 名前が変更されたシグナル
    name_changed = Signal()
    # 個数が変更されたシグナル
    number_changed = Signal()

    def __init__(self, parent: QObject = None) -> None:
        super().__init__(parent)
        self._name = ''
        self._number = 0

    @property
    def name(self) -> str:
        """名前."""
        return self._name

    def change_name(self, name: str) -> None:
        """名前を変更します.
        :param name: 名前
        """
        # ロジックに関わる処理は Model 側で行う
        if not name:
            return
        self._name = name
        self.name_changed.emit()

    @property
    def number(self) -> int:
        """個数."""
        return self._number

    def add_number(self, number: int) -> None:
        """個数を加算します.
        :param number: 加算する数
        """
        # ロジックに関わる処理は Model 側で行う
        if number < 0:
            return
        self._number += number
        self.number_changed.emit()


class ViewModel(QObject):
    """Model の内容を表示用に加工するクラス.
    :param model: Model オブジェクト
    :param parent: 親オブジェクト
    """
    # 名前が変更されたシグナル
    name_changed = Signal()
    # 個数が変更されたシグナル
    number_changed = Signal()

    def __init__(self, model: Model, parent: QObject = None) -> None:
        super().__init__(parent)
        self._model = model
        self._model.name_changed.connect(self._on_name_changed)
        self._model.number_changed.connect(self._on_number_changed)
        self._name = ''
        self._number = ''  # LineEdit に表示するので str 型になる

    @property
    def name(self) -> str:
        """名前."""
        return self._name

    @property
    def number(self) -> str:
        """個数."""
        return self._number

    def _on_name_changed(self) -> None:
        """名前が変更された."""
        # 表示用に加工して保持
        self._name = f'**{self._model.name}**'
        self.name_changed.emit()

    def _on_number_changed(self) -> None:
        """個数が変更された."""
        # 表示用に加工して保持
        self._number = f'{self._model.number} 個'
        self.number_changed.emit()


class View(QWidget):
    """表示クラス.
    :param viewmodel: ViewModel オブジェクト
    :param parent: 親オブジェクト
    """
    def __init__(self, viewmodel: ViewModel, parent: QObject = None):
        super().__init__(parent)
        self._viewmodel = viewmodel
        self._viewmodel.name_changed.connect(self._on_viewmodel_changed)
        self._viewmodel.number_changed.connect(self._on_viewmodel_changed)
        self._name = QLineEdit('')
        self._number = QLineEdit('')
        layout = QVBoxLayout()
        layout.addWidget(self._name)
        layout.addWidget(self._number)
        self.setLayout(layout)

    def _on_viewmodel_changed(self) -> None:
        """ViewModel が変更された."""
        # ViewModel の内容をそのまま表示する
        self._name.setText(self._viewmodel.name)
        self._number.setText(self._viewmodel.number)


if __name__ == '__main__':
    app = QApplication()
    model = Model(app)
    viewmodel = ViewModel(model)
    view = View(viewmodel)
    # Model を変更すると、View に反映される
    model.change_name('りんご')
    model.add_number(5)
    view.show()
    app.exec()
