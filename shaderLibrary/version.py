# -*- coding: utf-8 -*-
'''

01/2019 - Start Development
03/2019 - Test Release
04/2019 - 1.0.1 / Added version

'''

VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_PATCH = 1

version = '{}.{}.{}'.format(VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)
__version__ = version

__app__ = 'Arcane Shader Library'
qtWinName = 'Arcane:Qt_' + __app__ + '_ui'

__all__ = ['version', '__version__', '__app__', 'qtWinName']
