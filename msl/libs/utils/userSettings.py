# --------------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
#
# User Settings Class / Instanced as userUI
# This class handle load/save tool properties on a local user json file
# --------------------------------------------------------------------------------------------
import os
from sys import platform

from msl.libs.utils.json_util import load_json, save_json


class UserSettings(object):
    def __init__(self, tool_name):
        '''Manages saving UI settings for tools and saving on local drive
        Args:
            tool_name (string) : tool name, used for filename.ini
        '''
        self.tool_name = tool_name
        self.verifyPath()

    def verifyPath(self):
        ''' Check for root .ini files directory or make it '''
        dirPath = os.path.split(self.userPath)[0]
        if not os.path.exists(dirPath):
            print('Config .ini directory not found, making one:', dirPath)
            os.mkdir(dirPath)

    def saveUS(self, data):
        '''Saves a dictionary into a json file (windows user path)
        Args:
            data (dictionary) : info dictionary to save
        '''
        save_json(data, self.userPath)

    def loadUS(self):
        ''' Load json file from userPath and returns dict content '''
        return load_json(self.userPath)

    def loadProjectUS(self, project):
        ''' Load json file from userPath and returns dict content '''
        return load_json(self.userProjectPath(project))

    @property
    def userPath(self):
        ''' Returns user folder of this tool '''
        if platform == 'win32':
            return str(os.getenv('USERPROFILE')) + \
                '/ArcaneTools/' + self.tool_name + ".ini"
        else:
            return str(os.path.expanduser('~')) + \
                '/ArcaneTools/' + self.tool_name + ".ini"
