# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# Dialog Windows
# ----------------------------------------------------------------------------------------
from PySide2 import QtWidgets
import maya.cmds as cmds

from msl.libs.logger import log
from msl.ui.icons import get_icon


def warning_message(message: str):
    ''' open qt dialog box '''
    msg = QtWidgets.QMessageBox(None)
    msg.setStyleSheet("background: rgba(40, 40, 40, 255);")
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.setWindowIcon(get_icon('app'))
    msg.setText(message)
    msg.setWindowTitle('MSL')
    msg.setStandardButtons(QtWidgets.QMessageBox.Close)
    msg.exec_()


def dirty_file_dialog():
    ''' Ask user to save their current scene
    if it was modified since last save.
    '''
    if not cmds.file(query=True, modified=True):
        return

    msg = 'Current file is modified. Do you want to save this file?'
    result = cmds.confirmDialog(title='Save changes',
                                message=msg,
                                button=['yes', 'no'],
                                defaultButton='yes',
                                cancelButton='no',
                                dismissString='no')
    if result == 'yes':
        try:
            cmds.file(save=True, type='mayaAscii')
        except RuntimeError as e:
            log.error(e)
