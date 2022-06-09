# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# QtDesigner UI File loader for Maya PySide2 / Python 3
# ----------------------------------------------------------------------------------------

from PySide2 import QtWidgets
from shiboken2 import wrapInstance
from maya import OpenMayaUI as omui


def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
