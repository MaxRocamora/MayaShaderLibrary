# ------------------------------------------------------------------------
# Shader Library addShader dialog
# This class ask handles adding a new shader
# ------------------------------------------------------------------------
from PySide2 import QtWidgets

from msl.libs.shader import Shader as Shader
from msl.libs.dialogs.dlg_inform import informationDialog

msg_no_category = 'No categories found, create one using the Create Category button',
msg_overwrite = 'Shader name already exists, add a new copy?'
msg_failed_export = 'Add Shader save operation Failed.'


class addShaderDialog():

    def __init__(self, observer):
        ''' Add Shader Dialog
        Args:
            observer (class) observer holding ui/category
        '''
        self.observer = observer
        self.category = observer.selectedCategory

        if not self.category:
            informationDialog(msg_no_category, self.observer.ui)
            return

        shader, msg = Shader.getShader(self.category)
        if not shader:
            informationDialog(msg, self.observer.ui)
            return

        for s in self.category.shaders(reload=True):
            if s.name == shader['name']:
                overwrite = self.overwrite_shader_dialog(s.name)
                if not overwrite:
                    return
                break

        _shader = Shader.createShader(shader, self.category)
        if not _shader.save():
            informationDialog(msg_failed_export, self.observer.ui)
            return

        self.observer.main.categoryCC.refreshCategoryTab()

# --------------------------------------------------------------------------------------------
# addShader Support Dialogs
# --------------------------------------------------------------------------------------------

    def overwrite_shader_dialog(self, name):
        ''' open qt dialog box when shader already exists '''
        msgBox = QtWidgets.QMessageBox(self.observer.ui)
        msgBox.setStyleSheet("background: rgba(40, 40, 40, 255);")
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
        msgBox.setText(msg_overwrite)
        msgBox.setWindowTitle(name)
        msgBox.setStandardButtons(
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        choice = msgBox.exec_()
        return choice == QtWidgets.QMessageBox.Ok
