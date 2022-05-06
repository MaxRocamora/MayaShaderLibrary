# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
#
# Shader Class
# Get Shader from cg app using 'getShader' staticmethod
# use information returned from 'getShader'
# to create this class use 'createShader' classmethod.
#
# ----------------------------------------------------------------------------------------
import os
import json
import platform
import subprocess
import shutil
import datetime

import maya.cmds as cmds

from msl.libs.utils.json_util import load_json


class Shader():
    def __init__(self, name, category):
        ''' shader class
        Args:
            name (string) name of the shader
            category (class) category class
        '''
        self.properties = {}
        self._idName = name
        self._category = category
        self.ball = 'shdBall'

    def __str__(self):
        return f"Shader Class {self.name} , Category {self.category}"

# ----------------------------------------------------------------------------------------
# Properties
# ----------------------------------------------------------------------------------------

    @property
    def idName(self):
        return self._idName

    @property
    def name(self):
        return self.properties.get('name', '')

    @name.setter
    def name(self, v):
        self.properties['name'] = v

    @property
    def category(self):
        return self._category

    @property
    def user(self):
        return self.properties.get('User', 'N/A')

    @property
    def pc(self):
        return self.properties.get('PC', 'N/A')

    @property
    def folder(self):
        ''' physical path of ths shader '''
        return os.path.abspath(os.path.join(self.category.folder, self.idName))

    @property
    def cgFile(self):
        ''' return cg file path for this shader '''
        return os.path.join(self.folder, self.name + "_shader.ma")

    @property
    def configFile(self):
        ''' return config file path for this shader '''
        return os.path.join(self.folder, self.idName + "_shader.json")

    @property
    def hasProperties(self):
        ''' return if shader has a json properties file '''
        return os.path.exists(self.configFile)

    @property
    def shaderType(self):
        ''' node type or shader type for this shader '''
        return self.properties.get('shaderType', 'N/A')

    @shaderType.setter
    def shaderType(self, v):
        self.properties['shaderType'] = v

    @property
    def node(self):
        ''' node name for this shader '''
        return self.properties.get('node', 'N/A')

    @node.setter
    def node(self, v):
        self.properties['node'] = v

    @property
    def sourceFile(self):
        ''' source cgFile for this shader '''
        return self.properties.get('sourceFile', 'N/A')

    @sourceFile.setter
    def sourceFile(self, v):
        self.properties['sourceFile'] = v

    @property
    def maps(self):
        ''' list of texture files for this shader '''
        return self.properties.get('maps', '')

    @maps.setter
    def maps(self, v):
        self.properties['maps'] = v

    @property
    def notes(self):
        ''' custom notes for this asset '''
        return self.properties.get('notes', 'Enter notes here...')

    @notes.setter
    def notes(self, v):
        self.properties['notes'] = v

# --------------------------------------------------------------------------------------------
# Thumbnail
# --------------------------------------------------------------------------------------------

    @property
    def thumbnail_default(self):
        ''' Path to thumbnail file or default '''
        return os.path.join(os.path.dirname(__file__),
                            'resources',
                            'default_thumb.jpg'
                            )

    @property
    def thumbnail(self):
        ''' Path to thumbnail file or default '''
        return os.path.join(self.folder, self.name + '_thumb.png')

    def get_thumbnail(self):
        ''' return thumbnail file '''
        if os.path.exists(self.thumbnail):
            return self.thumbnail

        return self.thumbnail_default

# --------------------------------------------------------------------------------------------
# Load Methods
# --------------------------------------------------------------------------------------------

    def loadShaderProperties(self):
        ''' Load shaders properties from json file on disk '''
        self.properties = dict(load_json(self.configFile))

# --------------------------------------------------------------------------------------------
# Export Methods (MAYA)
# --------------------------------------------------------------------------------------------

    def save(self):
        ''' Takes this shader asset and export into file
        Creates folder, configFile, thumbnail, cg file and copy maps
        '''
        mementoSelection = cmds.ls(sl=True)
        print('Adding this shader {} into this category {}'.format(
            self.name, self.category.name))
        if cmds.objExists(self.ball):
            cmds.delete(self.ball)
        try:
            shadedBall = cmds.polySphere(name=self.ball)
            self.assignShader(self.ball)
        except TypeError as e:
            # if error is raised, delete the shader ball and abort saving.
            print(f'Error on assign shader to shadingBall ({str(e)})')
            cmds.delete(self.ball)
            return
        cmds.select(shadedBall, r=True)
        # Once the shader was successfully exported, make folder and files
        if not os.path.exists(self.folder):
            os.mkdir(os.path.abspath(self.folder))
        cmds.file(self.cgFile, type='mayaAscii',
                  exportSelected=True, force=True)
        cmds.delete(self.ball)
        # Copy maps (optional)
        self.saveShaderProperties()
        cmds.select(mementoSelection, r=True)
        return True

    def saveShaderProperties(self):
        ''' Save shaders properties into json file on disk '''
        if not self.hasProperties:
            dictData = {}
            try:
                with open(self.configFile, 'w') as loadedJsn:
                    json.dump(dictData, loadedJsn, sort_keys=True, indent=4)
            except OSError:
                print(f'Config File for shader {self.name} not found.')

        # opens and read json into dictData
        with open(self.configFile) as loadedJsn:
            dictData = json.load(loadedJsn)
            dictData["idName"] = self.idName
            dictData["name"] = self.name
            dictData["category"] = self.category.name
            dictData["notes"] = self.notes
            dictData["sourceFile"] = self.sourceFile
            dictData["maps"] = self.maps
            dictData["node"] = self.node
            dictData["shaderType"] = self.shaderType
            dictData['PC'] = str(platform.node())
            dictData['User'] = str(os.getenv('username'))
            dictData['Edited On'] = str(datetime.datetime.now())
        with open(self.configFile, 'w') as loadedJsn:
            json.dump(dictData, loadedJsn, sort_keys=True, indent=4)

# --------------------------------------------------------------------------------------------
# Import Methods (MAYA)
# --------------------------------------------------------------------------------------------

    def importShader(self, assign=False):
        '''
        imports shader into scene
        Args:
            assign (boolean) if true, try to assign shader to selected mesh
        '''
        sel = cmds.ls(sl=True)
        if cmds.objExists(self.name):
            print('shader is in scene, ask for replace', self.name)
        else:
            cmds.file(self.cgFile, type='mayaAscii', i=True, force=True)

        try:
            if assign:
                self.assignShader(sel)
        except TypeError as e:
            print(str(e))
        finally:
            if cmds.objExists(self.ball):
                cmds.delete(self.ball)
        cmds.select(sel, r=True)

    def assignShader(self, items=None):
        ''' Assign the shader to the given item '''
        shaderSG = self.getSG()
        if items and shaderSG:
            cmds.sets(items, e=True, forceElement=shaderSG)

    def getSG(self):
        ''' gets shading group of this shader '''
        if cmds.objExists(self.node):
            shaderSGConn = cmds.listConnections(
                self.node, d=True, et=True, t='shadingEngine')
            if shaderSGConn:
                return shaderSGConn[0]
        return False

# --------------------------------------------------------------------------------------------
# Delete/Rename/Browse Methods
# --------------------------------------------------------------------------------------------

    def rename(self, newName=False):
        ''' rename cg file and config file and this class '''
        if not newName:
            return False

        oldConfigFile = self.configFile
        oldCGFile = self.cgFile
        oldThumbFile = self.thumbnail
        self.properties['name'] = newName
        os.rename(oldConfigFile, self.configFile)
        os.rename(oldCGFile, self.cgFile)
        if os.path.exists(oldThumbFile):
            os.rename(oldThumbFile, self.thumbnail)
        self.saveShaderProperties()
        return True

    def delete(self):
        ''' deletes this shader from disk '''
        if os.path.exists(self.folder):
            print('Deleting Folder:', self.folder)
            shutil.rmtree(self.folder)

    def browse(self):
        ''' Open current shader folder '''
        location = os.path.abspath(self.folder)
        if os.path.exists(location):
            subprocess.Popen("explorer " + location)

# --------------------------------------------------------------------------------------------
# Generate Methods
# --------------------------------------------------------------------------------------------

    @staticmethod
    def loadShader(name, category):
        '''
        Use this method to load a shader from disk.
        Args:
            name (string): name of the internal folder of this shader
        Returns:
            shader class object
        '''
        shader = Shader(name, category)
        shader.loadShaderProperties()
        return shader

    @staticmethod
    def createShader(shaderData, category):
        ''' Use this method to create a virtual shader,
        sets own attributes and returns this class.
        the id is generated by taking the last free folder
        from 'SHD_0000' pattern.
        Args:
            shaderData (dic) Contains all values from getShader() staticmethod
            category (class) parent category
        '''
        nextId = 0
        while 'SHD_' + str(nextId).zfill(4) in os.listdir(category.folder):
            nextId += 1
        name = 'SHD_' + str(nextId).zfill(4)
        shader = Shader(name, category)
        shader.name = shaderData['name']
        shader.node = shaderData['node']
        shader.shaderType = shaderData['shaderType']
        shader.maps = shaderData['maps']
        shader.sourceFile = shaderData['sourceFile']
        return shader

    @staticmethod
    def getShader(category):
        '''
        Use this method to get selected shader from cg app
        After get the current shader, fill shaderData dict with
        necessary information and returns it.
        Args:
            category (string): category of this shader
        Returns:
            shaderData (dic): info from shader or False
            msg (string): error message
        '''
        ignoreDefaults = ['lambert1', 'particleCloud1',
                          'shaderGlow1', 'defaultColorMgtGlobals']
        app = 'maya'
        shaderData = {'name': 'default',
                      'maps': [],
                      'app': app,
                      'node': 'defaultNode',
                      'shaderType': 'N/A'
                      }

        selection = cmds.ls(sl=True)
        if len(selection) == 0:
            return False, 'Nothing Selected!'
        elif len(selection) > 1:
            return False, 'Multiple objects selected!'
        selType = cmds.nodeType(selection[0])
        if selType == 'transform':
            shape = cmds.ls(dag=1, o=1, s=1, sl=1)
            sg = cmds.listConnections(shape, type='shadingEngine')
            shaders = cmds.ls(cmds.listConnections(sg), materials=1)
            if len(shaders) == 0:
                return False, 'No shader found on selected object'
        else:
            isShader = cmds.getClassification(selType, satisfies="shader")
            shaders = [selection[0]]
            if not isShader:
                return False, f'No shader found for type ({selType})'

        if shaders[0] in ignoreDefaults:
            msg = f'Shader found is maya default ({shaders[0]})'
            return False, msg

        shaderData['name'] = shaders[0]
        shaderData['node'] = shaders[0]
        shaderData['maps'] = ['maps1', 'maps2']
        shaderData['shaderType'] = cmds.nodeType(shaders[0])
        shaderData['sourceFile'] = cmds.file(
            query=True, sceneName=True, shortName=True)
        shaderData['category'] = category.name

        return shaderData, 1
