# --------------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# Observer is a singleton Class holding UI, Categories, and Selected Shader
# When a shader is selected, the shader clicked signal
# sends itself to this class using 'selected_shader'
# property and updates ui texts
# ----------------------------------------------------------------------------------------
from msl.libs.logger import log
from msl.libs.utils.singleton import Singleton


class Observer(Singleton):
    def __init__(self):
        self._shader = False
        self._category = False
        self._categories = []
        # self.ui (holds main ui)
        # self.view (hold view class)

    def categories(self):
        return self._categories

    def set_categories(self, v):
        ''' load given categories and updates view '''
        self._categories = v
        self.view.update_view(v)

    def category(self):
        ''' current selected category'''
        return self._category

    def select_category(self, v):
        self._category = v
        if not v:
            self.shader = False
            return
        log.info(f'Category selected: {v.name()} Shaders {len(v.shaders())}')

    def shader(self):
        ''' current selected shader '''
        return self._shader

    def select_shader(self, v):
        self._shader = v
        self.update_UI()

    def update_UI(self):
        ''' update ui when user selects a shader '''
        self.ui.lbl_shader_name.setText(
            f'{self.shader().name} / {self.shader().category.name()}')
        self.ui.lbl_shader_type.setText(self.shader().shader_type)
        self.ui.te_notes.setText(self.shader().notes)
