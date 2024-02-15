# ------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# Shader Class
# Get Shader from disk using 'get_shader' staticmethod
# use information returned from 'get_shader'
# To create this class use 'create_shader()' classmethod.
#
# ----------------------------------------------------------------------------------------
import os
import json
import shutil
import datetime
from typing import TYPE_CHECKING

import maya.cmds as cmds

from msl.libs.utils.json_util import load_json
from msl.libs.utils.folder import browse
from msl.libs.logger import log

if TYPE_CHECKING:
    from msl.libs.category import Category


class Shader:
    def __init__(self, name: str, category: 'Category'):
        """Shader class.

        Args:
            name (str): name of the shader
            category (class): category class
        """
        self.properties = {}
        self._id_name = name
        self._category = category
        self.ball = 'shdBall'

    def __str__(self):
        """String representation of this class."""
        return f'Shader Class {self.name} , Category {self.category}'

    # ------------------------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------------------------

    @property
    def id_name(self) -> str:
        """Return the id name of this shader."""
        return self._id_name

    @property
    def name(self) -> str:
        """Name of this shader."""
        return self.properties.get('name', '')

    @name.setter
    def name(self, value: str):
        """Set the name of this shader."""
        self.properties['name'] = value

    @property
    def category(self) -> str:
        """Return the category of this shader."""
        return self._category

    @property
    def user(self) -> str:
        """Return the user of this shader."""
        return self.properties.get('User', 'N/A')

    @property
    def pc(self) -> str:
        """Return the pc of this shader."""
        return self.properties.get('PC', 'N/A')

    @property
    def folder(self) -> str:
        """Physical path of ths shader."""
        return os.path.abspath(os.path.join(self.category.path(), self.id_name))

    @property
    def cg_file(self) -> str:
        """Return cg file path for this shader."""
        return os.path.join(self.folder, self.name + '_shader.ma')

    @property
    def config_file(self) -> str:
        """Return config file path for this shader."""
        return os.path.join(self.folder, 'shader.json')

    @property
    def has_properties(self) -> bool:
        """Return if shader has a json properties file."""
        return os.path.exists(self.config_file)

    @property
    def shader_type(self) -> str:
        """Node type or shader type for this shader."""
        return self.properties.get('shaderType', 'N/A')

    @shader_type.setter
    def shader_type(self, value: str):
        self.properties['shaderType'] = value

    @property
    def node(self) -> str:
        """Node name for this shader."""
        return self.properties.get('node', 'N/A')

    @node.setter
    def node(self, value: str):
        self.properties['node'] = value

    @property
    def source_file(self) -> str:
        """Source cgFile for this shader."""
        return self.properties.get('sourceFile', 'N/A')

    @source_file.setter
    def source_file(self, value: str):
        self.properties['sourceFile'] = value

    @property
    def maps(self) -> list:
        """List of texture files for this shader."""
        return self.properties.get('maps', '')

    @maps.setter
    def maps(self, value: list):
        self.properties['maps'] = value

    @property
    def notes(self) -> str:
        """Custom notes for this asset."""
        return self.properties.get('notes', 'Enter notes here...')

    @notes.setter
    def notes(self, value: str):
        self.properties['notes'] = value

    # ------------------------------------------------------------------------------------
    # Thumbnail
    # ------------------------------------------------------------------------------------

    @property
    def thumbnail_default(self) -> str:
        """Path to thumbnail file or default."""
        return os.path.join(
            os.path.dirname(__file__), 'resources', 'img', 'default_thumb.jpg'
        )

    @property
    def thumbnail(self) -> str:
        """Path to thumbnail file or default."""
        return os.path.join(self.folder, self.name + '_thumb.png')

    def get_thumbnail(self) -> str:
        """Return thumbnail file."""
        if os.path.exists(self.thumbnail):
            return self.thumbnail

        return self.thumbnail_default

    # ------------------------------------------------------------------------------------
    # Load Methods
    # ------------------------------------------------------------------------------------

    def load_shader_properties(self) -> dict:
        """Load shaders properties from json file on disk."""
        try:
            self.properties = dict(load_json(self.config_file))
        except TypeError:
            self.properties = {}

    # ------------------------------------------------------------------------------------
    # Export Methods (MAYA)
    # ------------------------------------------------------------------------------------

    def save(self):
        """Saves this shader into disk, creates folder, and json."""

        memento_selection = cmds.ls(sl=True)

        log.info(f'Adding shader {self.name} into this category {self.category.name()}')

        if cmds.objExists(self.ball):
            cmds.delete(self.ball)

        try:
            shadedBall = cmds.polySphere(name=self.ball)
            self.assign_shader(self.ball)
        except TypeError as e:
            # if error is raised, delete the shader ball and abort saving.
            log.warning(f'Error on assign shader to shadingBall ({str(e)})')
            cmds.delete(self.ball)
            return

        cmds.select(shadedBall, r=True)

        # Once the shader was successfully exported, make folder and files
        if not os.path.exists(self.folder):
            os.mkdir(os.path.abspath(self.folder))

        cmds.file(self.cg_file, type='mayaAscii', exportSelected=True, force=True)
        cmds.delete(self.ball)

        self.save_shader_properties()
        cmds.select(memento_selection, r=True)

        return True

    def save_shader_properties(self):
        """Save shaders properties into json file on disk."""
        if not self.has_properties:
            dictData = {}
            try:
                with open(self.config_file, 'w') as _json:
                    json.dump(dictData, _json, sort_keys=True, indent=4)
            except OSError:
                log.error(f'Config File for shader {self.name} not found.')

        # opens and read json into dictData
        with open(self.config_file) as _json:
            dictData = json.load(_json)
            dictData['id_name'] = self.id_name
            dictData['name'] = self.name
            dictData['category'] = self.category.name()
            dictData['notes'] = self.notes
            dictData['sourceFile'] = self.source_file
            dictData['maps'] = self.maps
            dictData['node'] = self.node
            dictData['shaderType'] = self.shader_type
            dictData['Edited On'] = str(datetime.datetime.now())

        with open(self.config_file, 'w') as _json:
            json.dump(dictData, _json, sort_keys=True, indent=4)

    # ------------------------------------------------------------------------------------
    # Import Methods (MAYA)
    # ------------------------------------------------------------------------------------

    def import_shader(self, assign: bool = False):
        """Imports shader into scene.

        Args:
            assign (bool): if true, try to assign shader to selected mesh
        """
        sel = cmds.ls(sl=True)
        if cmds.objExists(self.name):
            log.info(f'Shader exists in scene, asking for replace {self.name}')
        else:
            cmds.file(self.cg_file, type='mayaAscii', i=True, force=True)

        try:
            if assign:
                self.assign_shader(sel)
        except TypeError as e:
            log.info(str(e))
        finally:
            if cmds.objExists(self.ball):
                cmds.delete(self.ball)

        cmds.select(sel, r=True)

    def assign_shader(self, items: list = None):
        """Assign the shader to the given item."""
        sg = self.get_shading_group()
        if items and sg:
            cmds.sets(items, e=True, forceElement=sg)

    def get_shading_group(self) -> str:
        """Gets shading group of this shader."""
        if cmds.objExists(self.node):
            shaderSGConn = cmds.listConnections(
                self.node, d=True, et=True, t='shadingEngine'
            )
            if shaderSGConn:
                return shaderSGConn[0]

        return False

    # ------------------------------------------------------------------------------------
    # Delete/Rename/Browse Methods
    # ------------------------------------------------------------------------------------

    def rename(self, new_name: str = False) -> bool:
        """Rename cg file and config file and this class."""
        if not new_name:
            return False

        _old_CG_file = self.cg_file
        _old_thumb_file = self.thumbnail
        self.properties['name'] = new_name
        os.rename(_old_CG_file, self.cg_file)

        if os.path.exists(_old_thumb_file):
            os.rename(_old_thumb_file, self.thumbnail)

        self.save_shader_properties()

        return True

    def delete(self):
        """Deletes this shader from disk."""
        if os.path.exists(self.folder):
            print('Deleting Folder:', self.folder)
            shutil.rmtree(self.folder)

    def explore(self):
        """Open Category folder."""
        browse(self.folder)

    # ------------------------------------------------------------------------------------
    # Generate Methods
    # ------------------------------------------------------------------------------------

    @staticmethod
    def load_shader(name: str, category: 'Category') -> 'Shader':
        """Use this method to load a shader from disk.

        Args:
            name (str): name of the internal folder of this shader
            category (Category): category class
        Returns:
            Shader object
        """
        shader = Shader(name, category)
        shader.load_shader_properties()
        return shader

    @staticmethod
    def create_shader(shader_data: dict, category: 'Category') -> 'Shader':
        """Use this method to create a virtual shader.

        Sets own attributes and returns this class.
        the id is generated by taking the last free folder
        from 'SHD_0000' pattern.

        Args:
            shader_data (dict): Contains all values from getShader() staticmethod
            category (Category): parent category
        """
        nextId = 0

        while 'SHD_' + str(nextId).zfill(4) in os.listdir(category.path()):
            nextId += 1

        name = 'SHD_' + str(nextId).zfill(4)

        shader = Shader(name, category)
        shader.name = shader_data['name']
        shader.node = shader_data['node']
        shader.shaderType = shader_data['shaderType']
        shader.maps = shader_data['maps']
        shader.sourceFile = shader_data['sourceFile']

        return shader

    @staticmethod
    def get_shader(category: 'Category') -> tuple:
        """Use this method to get selected shader from viewport selection.

        After get the current shader, fill shader_data dict with
        necessary information and returns it.

        Args:
            category (Category): category of this shader

        Returns:
            shader_data (dict): info from shader or False
            msg (string): error message
        """
        ignore_defaults = [
            'lambert1',
            'particleCloud1',
            'shaderGlow1',
            'defaultColorMgtGlobals',
        ]
        app = 'maya'
        shader_data = {
            'name': 'default',
            'maps': [],
            'app': app,
            'node': 'defaultNode',
            'shaderType': 'N/A',
        }

        selection = cmds.ls(sl=True)
        if not selection:
            return False, 'Nothing Selected!'

        if len(selection) > 1:
            return False, 'Multiple objects selected!'

        sel_type = cmds.nodeType(selection[0])
        if sel_type == 'transform':
            shape = cmds.ls(dag=1, o=1, s=1, sl=1)
            sg = cmds.listConnections(shape, type='shadingEngine')
            shaders = cmds.ls(cmds.listConnections(sg), materials=1)
            if len(shaders) == 0:
                return False, 'No shader found on selected object'
        else:
            isShader = cmds.getClassification(sel_type, satisfies='shader')
            shaders = [selection[0]]
            if not isShader:
                return False, f'No shader found for type ({sel_type})'

        if shaders[0] in ignore_defaults:
            msg = f'Shader found is maya default ({shaders[0]})'
            return False, msg

        shader_data['name'] = shaders[0]
        shader_data['node'] = shaders[0]
        shader_data['shaderType'] = cmds.nodeType(shaders[0])
        shader_data['sourceFile'] = cmds.file(query=True, sceneName=True, shortName=True)
        shader_data['category'] = category.name
        shader_data['maps'] = ['maps1', 'maps2']  # ! maps not implemented

        return shader_data, 1
