# -*- coding: utf-8 -*-
'''
ARCANE Category Class
Category main object

'''

# IMPORTS
import os
import subprocess
from msl import LIBRARY_SHADERS_PATH
from .dialogs.dlg_inform import informationDialog
from .shader import Shader as Shader


class Category(object):
    def __init__(self, category, path):
        ''' When a category is created, stores all its shaders '''
        self._name = category
        self.baseFolder = path
        self._shaders = self.collectShaders()

    def __str__(self):
        return "Category Class {}".format(self.name)

# --------------------------------------------------------------------------------------------
# Properties
# --------------------------------------------------------------------------------------------

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

# --------------------------------------------------------------------------------------------
# Collect / Generate Methods
# --------------------------------------------------------------------------------------------

    def collectShaders(self):
        ''' Returs a list of shader objects from chosen category '''
        shaderFolders = [x.upper() for x in os.listdir(self.folder)]
        shaders = []

        for f in shaderFolders:
            shaders.append(Shader.loadShader(name=f, category=self))
        return shaders

# --------------------------------------------------------------------------------------------
# Static Methods
# --------------------------------------------------------------------------------------------

    @staticmethod
    def create(name):
        ''' create category folder '''
        if os.path.exists(LIBRARY_SHADERS_PATH):
            os.mkdir(os.path.abspath(os.path.join(LIBRARY_SHADERS_PATH, name)))

    @staticmethod
    def collectCategorys(ui):
        ''' Load Categorys from disk and set up main storing list '''
        categorys = []
        if os.path.exists(LIBRARY_SHADERS_PATH):
            categoryFolders = [x.upper() for x in os.listdir(LIBRARY_SHADERS_PATH)]
            if len(categoryFolders) > 0:
                for index, name in enumerate(categoryFolders):
                    categorys.append(Category(name, LIBRARY_SHADERS_PATH))
        else:
            informationDialog("Warning: Categorys Folder not found.", ui)
            print 'Path Searched:', LIBRARY_SHADERS_PATH
        return categorys
