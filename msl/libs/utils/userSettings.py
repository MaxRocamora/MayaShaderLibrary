# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------
#
# User Settings Class / Instanced as userUI
# Pass tool name on creation, this class handle load/save tool properties
# on a local user json file
# --------------------------------------------------------------------------------------------
from __future__ import print_function
import os
from sys import platform

from jsonHelp import getDictJson, saveDictJson

# --------------------------------------------------------------------------------------------
# Class: Main UI
# --------------------------------------------------------------------------------------------


class UserSettings(object):
    def __init__(self, _toolName):
        '''
        Manages saving UI settings for tools and saving on local drive
        Args:
            _toolName (string) : tool name, used for filename.ini
        '''
        self.toolName = _toolName
        self.verifyPath()

    def verifyPath(self):
        ''' Check for root .ini files directory or make it '''
        dirPath = os.path.split(self.userPath)[0]
        if not os.path.exists(dirPath):
            print('Config .ini directory not found, making one:', dirPath)
            os.mkdir(dirPath)

    def saveUS(self, data):
        '''
        Saves a dictionary into a json file (windows user path)
        Args:
            data (dictionary) : info dictionary to save
        '''
        saveDictJson(data, self.userPath)

    def loadUS(self):
        ''' Load json file from userPath and returns dict content '''
        return getDictJson(self.userPath)

    def loadProjectUS(self, project):
        ''' Load json file from userPath and returns dict content '''
        return getDictJson(self.userProjectPath(project))

    @property
    def userPath(self):
        ''' Returns user folder of this tool '''
        if platform == 'win32':
            return str(os.getenv('USERPROFILE')) + \
                '/ArcaneTools/' + self.toolName + ".ini"
        else:
            return str(os.path.expanduser('~')) + \
                '/ArcaneTools/' + self.toolName + ".ini"
