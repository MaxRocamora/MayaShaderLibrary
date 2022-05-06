# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
#
# Category Class
#
# ----------------------------------------------------------------------------------------
import os
import subprocess

from msl import LIBRARY_SHADERS_PATH
from msl.libs.dialogs.dlg_inform import informationDialog
from msl.libs.shader import Shader as Shader


class Category():
    def __init__(self, category, path):
        ''' When a category is created, stores all its shaders '''
        self._name = category
        self.baseFolder = path
        self._shaders = self.collectShaders()

    def __str__(self):
        return "Category Class {}".format(self.name)

    # ------------------------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------------------------

    @property
    def name(self):
        return self._name

    @property
    def folder(self):
        ''' physical path of ths shader '''
        return os.path.abspath(os.path.join(self.baseFolder, self.name))

    def shaders(self, reload=False):
        '''
        Return list of shaders of this category
        Args:
            reload (boolean): If true, reload shaders from disk before return
        Returns:
            list: shaders objects
        '''
        if reload:
            self._shaders = self.collectShaders()
        return self._shaders

    def browse(self):
        ''' Open current shader folder '''
        location = os.path.abspath(self.folder)
        if os.path.exists(location):
            subprocess.Popen("explorer " + location)

    # ------------------------------------------------------------------------------------
    # Collect / Generate Methods
    # ------------------------------------------------------------------------------------

    def collectShaders(self):
        ''' Returns a list of shader objects from chosen category '''
        folders = [x.upper() for x in os.listdir(self.folder)]
        return [Shader.loadShader(name=f, category=self) for f in folders]

    # ------------------------------------------------------------------------------------
    # Static Methods
    # ------------------------------------------------------------------------------------

    @staticmethod
    def create(name):
        ''' create category folder '''
        if os.path.exists(LIBRARY_SHADERS_PATH):
            os.mkdir(os.path.abspath(os.path.join(LIBRARY_SHADERS_PATH, name)))

    @staticmethod
    def collectCategories(ui):
        ''' Load Categories from disk and set up main storing list '''
        if not os.path.exists(LIBRARY_SHADERS_PATH):
            informationDialog("Warning: Categories Folder not found.", ui)
            print('Path:', LIBRARY_SHADERS_PATH)
            return []

        folders = [x.upper() for x in os.listdir(LIBRARY_SHADERS_PATH)]
        if not folders:
            return []

        return [Category(name, LIBRARY_SHADERS_PATH) for name in folders]
