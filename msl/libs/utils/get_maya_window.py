# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# QtDesigner UI File loader for Maya PySide2/6 / Python 3
# ----------------------------------------------------------------------------------------

from maya import OpenMayaUI

try:
    from PySide2 import QtWidgets
    from shiboken2 import wrapInstance
except ImportError:
    from PySide6 import QtWidgets
    from shiboken6 import wrapInstance


def get_maya_main_window():
    """Get the main Maya window as a QMainWindow instance."""
    main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
