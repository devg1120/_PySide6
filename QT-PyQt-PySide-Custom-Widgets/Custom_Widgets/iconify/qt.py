"""
Expose Qt to iconify using the ICONIFY_QTLIB environment variable.
"""

import os
import pydoc
from typing import TYPE_CHECKING

#import qtpy
#from qtpy import QtCore, QtGui, QtSvg, QtWidgets, QtXml

from PySide6 import *                                         
from PySide6.QtWidgets import *                                         
from PySide6.QtCore import *                               
from PySide6.QtGui import *                 
from PySide6.QtUiTools import *            



#if 'pyside2' in qtpy.API:
#    qtlib = 'pyside2'
#elif 'pyside6' in qtpy.API:
#    qtlib = 'pyside6'
qtlib = 'pyside6'


_IMPORT_ERROR_MESSAGE = \
    "Unable to import required Qt libraries from {0}! Please set the " \
    "'ICONIFY_QTLIB' env var to the location of a Qt5 compliant python " \
    "binding you would like to use."

if None in (QtCore, QtGui, QtSvg, QtWidgets, QtXml):
    raise ImportError(_IMPORT_ERROR_MESSAGE.format(qtlib))
