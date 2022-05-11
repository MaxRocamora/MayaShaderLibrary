# --------------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# Observer its loaded by the main app
# Holds selected shader from UI and the main UI
# When a shader is selected, the shader clicked signal
# sends itself to this class using 'selectedShader'
# property and updates ui texts
# ----------------------------------------------------------------------------------------
from msl.libs.logger import log


class ObserverUI():
    def __init__(self, main, ui):
        self.main = main
        self.ui = ui
        self.shader = False
        self.category = False
        self._categories = []

    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, v):
        self._categories = v

    @property
    def selected_category(self):
        return self.category

    @selected_category.setter
    def selected_category(self, v):
        self.category = v
        if not v:
            self.shader = False
            return
        log.info(f'Category selected: {v.name()} Shaders {len(v.shaders())}')

    @property
    def selected_shader(self):
        return self.shader

    @selected_shader.setter
    def selected_shader(self, v):
        self.shader = v
        self.update_UI()

    def update_UI(self):
        ''' update ui when user selects a shader '''
        self.ui.lbl_shader_name.setText(
            f'{self.shader.name} / {self.shader.category.name()}')
        self.ui.lbl_shader_type.setText(self.shader.shader_type)
        self.ui.lbl_shader_user_pc.setText(f'{self.shader.user} / {self.shader.pc}')
        self.ui.lbl_shader_code.setText(self.shader.id_name)
        self.ui.te_notes.setText(self.shader.notes)
