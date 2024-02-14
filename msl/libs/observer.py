# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# Observer is a singleton Class holding UI, Categories, and Selected Shader
# When a shader is selected, the shader clicked signal
# sends itself to this class using .selected_shader() and updates ui shader info
# Note:
# .ui attribute is set from main
# ----------------------------------------------------------------------------------------
from typing import TYPE_CHECKING

from msl.libs.logger import log
from msl.libs.utils.singleton import Singleton

if TYPE_CHECKING:
    from msl.libs.category import Category


class Observer(Singleton):
    def __init__(self):
        """Observer class."""
        self._shader = False
        self._category = False

    def category(self):
        """Current selected category."""
        return self._category

    def select_category(self, category: 'Category'):
        """Select a category from the list and updates UI."""
        self._category = category
        log.info(f'Category selected: {category.name()} Shaders {len(category)}')

    def shader(self):
        """Current selected shader."""
        return self._shader

    def select_shader(self, value: str):
        """Select a shader from the list and updates UI."""
        log.info(f'shader selected {value}')
        self._shader = value
        self.update_UI()

    def update_UI(self):
        """Update ui when user selects a shader."""
        if not self.shader():
            return

        self.ui.lbl_shader_name.setText(
            f'{self.shader().name} / {self.shader().category.name()}'
        )
        self.ui.lbl_shader_type.setText(self.shader().shader_type)
        self.ui.te_notes.setText(self.shader().notes)
        self.ui.lbl_shader_code.setText(self.shader().id_name)

    def status_message(self, msg: str):
        """Writes a message into the statusbar."""
        self.ui.statusBar().showMessage(msg)
