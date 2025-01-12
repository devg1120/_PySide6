import inspect
from PySide6.QtWidgets import QApplication, QSpinBox

def fun(i):
    print("This works, but why?", i)

def my_decorator(inner):
    signature = inspect.signature(inner)

    def wrapper(*args, **kwargs):
        try:
            signature.bind(*args, **kwargs)
        except TypeError:
            return inner()
        return inner(*args, **kwargs)
    return wrapper

@my_decorator
def decorated_fun():
    print("This fails")

app = QApplication()
box = QSpinBox()
box.valueChanged.connect(fun)
box.valueChanged.connect(decorated_fun)
box.setValue(10)
