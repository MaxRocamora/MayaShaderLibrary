# -*- coding: utf-8 -*-
'''Style QT Methods for Arcane Interfaces'''

from PySide2 import QtCore, QtGui

from msl import QSS_FILE, ICON_FILE


def cssMainWindow(mainWidget, objName, windowTitle):
    ''' Set QT CSS Stylesheet for QMainWindow
    Args:
        mainWidget (widget) main class (passed as self)
        objName (string) Name of the qt object for window detection/destroy.
        windowTitle (string) Set the name of the main window
    '''
    mainWidget.setWindowIcon(QtGui.QIcon(ICON_FILE))
    mainWidget.setObjectName(objName)
    mainWidget.setWindowTitle(windowTitle)
    mainWidget.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
    with open(QSS_FILE, "r") as fh:
        mainWidget.setStyleSheet(fh.read())
