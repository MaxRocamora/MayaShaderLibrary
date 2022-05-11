# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# Category Class
#
# ----------------------------------------------------------------------------------------
import os
import subprocess

from msl.config import LIBRARY_SHADERS_PATH
from msl.libs.dialogs.dlg_inform import information_dialog
from msl.libs.shader import Shader as Shader
from msl.libs.logger import log


class Category():
    def __init__(self, category, path):
        ''' When a category is created, stores all its shaders '''
        self._name = category
        self._path = path
        self._shaders = self.collect_shaders()

    def __str__(self):
        return f"Category: {self.name()}"

    def name(self):
        return self._name

    def folder(self):
        ''' physical path of ths shader '''
        return os.path.abspath(os.path.join(self._path, self.name()))

    def shaders(self, _reload=False):
        ''' Returns list of shaders of this category
        Args:
            _reload (boolean): If true, reload shaders from disk before return
        Returns:
            list: shaders objects
        '''
        if _reload:
            self._shaders = self.collect_shaders()
        return self._shaders

    def browse(self):
        ''' Open current shader folder '''
        location = os.path.abspath(self.folder())
        if os.path.exists(location):
            subprocess.Popen("explorer " + location)

    def collect_shaders(self):
        ''' Returns a list of shader objects from chosen category '''
        folders = [x.upper() for x in os.listdir(self.folder())]
        return [Shader.load_shader(name=f, category=self) for f in folders]

    # ------------------------------------------------------------------------------------
    # Static Methods
    # ------------------------------------------------------------------------------------

    @staticmethod
    def create(name):
        ''' create category folder '''
        if os.path.exists(LIBRARY_SHADERS_PATH):
            os.mkdir(os.path.abspath(os.path.join(LIBRARY_SHADERS_PATH, name)))

    @staticmethod
    def collect_categories(ui):
        ''' Load Categories from disk and set up main storing list '''
        if not os.path.exists(LIBRARY_SHADERS_PATH):
            information_dialog("Warning: Categories Folder not found.", ui)
            log.warning('Path:', LIBRARY_SHADERS_PATH)
            return []

        folders = [x.upper() for x in os.listdir(LIBRARY_SHADERS_PATH)]
        if not folders:
            return []

        return [Category(name, LIBRARY_SHADERS_PATH) for name in folders]
