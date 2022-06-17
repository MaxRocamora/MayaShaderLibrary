# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
#
# User Settings Class / Instanced as userUI
# This class handle load/save tool properties on a local user json file
# ----------------------------------------------------------------------------------------
import os
from sys import platform

from msl.libs.utils.json_util import load_json, save_json
from msl.libs.logger import log


class UserSettings():
    def __init__(self, tool_name):
        '''Manages saving UI settings for tools and saving on local drive
        Args:
            tool_name (string) : tool name, used for filename.ini
        '''
        self.tool_name = tool_name
        self._verify_user_path()

    def _verify_user_path(self):
        ''' Check for root .ini files directory or make it '''
        dir_path = os.path.split(self.user_path)[0]
        if not os.path.exists(dir_path):
            log.warning(f'Config .ini directory not found, making one into {dir_path}')
            os.mkdir(dir_path)

    def save(self, data):
        '''Saves a dictionary into a json file (windows user path)
        Args:
            data (dictionary) : info dictionary to save
        '''
        save_json(data, self.user_path)

    def load(self):
        ''' Load json file from user_path and returns dict content '''
        return load_json(self.user_path)

    @property
    def user_path(self):
        ''' Returns windows or mac user folder of this tool '''
        if platform == 'win32':
            return str(os.getenv('USERPROFILE')) + \
                '/ArcaneTools/' + self.tool_name + ".ini"
        else:
            return str(os.path.expanduser('~')) + \
                '/ArcaneTools/' + self.tool_name + ".ini"
