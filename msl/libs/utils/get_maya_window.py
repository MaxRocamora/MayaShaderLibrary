# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------
# QtDesigner UI File loader for Maya PySide2
# Python 2/3
# --------------------------------------------------------------------------------------------

import sys
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
from maya import OpenMayaUI as omui

PY_VERSION = sys.version_info.major

if PY_VERSION == 2:
    from cStringIO import StringIO
    import xml.etree.ElementTree as xml
    import pyside2uic as pysideuic


def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    if PY_VERSION >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)
