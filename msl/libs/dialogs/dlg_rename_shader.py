# ----------------------------------------------------------------------------------------
# ARCANE Shader Library renameShader dialog
#
# This class ask for user a new shader name, and handles errors
# ----------------------------------------------------------------------------------------

from PySide2.QtWidgets import QInputDialog, QLineEdit

from msl.libs.qt_dialogs import warning_message

msgStr = {
    'unicode_error': 'New name has a UnicodeEncodeError!',
    'length_error': 'New Shader name needs at least 4 characters.',
    'name_exists': 'Shader name already in use.'
}


class RenameShaderDialog(QInputDialog):

    def __init__(self, shader: type, observer: type):
        '''
        QInput dialog class for user rename shader action
        Args:
            shader (class) shader class calling this input
            observer (class) observer holding ui
        '''
        super().__init__()
        self.observer = observer
        self.shader = shader

    def __call__(self):
        ''' open qt dialog box for rename shader '''
        title = "Rename Shader"
        question = 'Enter Shader New Name'
        lineEdit = QLineEdit.Normal
        new_name, result = QInputDialog.getText(
            self.observer.ui, title, question, lineEdit, "default")
        if not result:
            return False
        try:
            new_name = str(new_name)
        except (UnicodeEncodeError, UnicodeDecodeError):
            warning_message(msgStr['unicode_error'])
            return False
        if len(new_name) <= 3:
            warning_message(msgStr['length_error'])
            return False
        if self.name_in_use(new_name):
            warning_message(msgStr['name_exists'])
            return False
        else:
            if self.shader.rename(new_name):
                self.shader.category.reload()

    def name_in_use(self, name: str):
        ''' returns true if shader new name is already in use '''
        return any(
            shader.name == name for shader in self.shader.category.shaders()
        )
