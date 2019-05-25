# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------
# QtDesigner UI File loader for Maya Pyside2
# --------------------------------------------------------------------------------------------

from cStringIO import StringIO
import xml.etree.ElementTree as xml
import maya.OpenMayaUI as om
from PySide2 import QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import shiboken2 as shiboken
import pyside2uic


def getMayaWindow():
    maya_window_util = om.MQtUtil.mainWindow()
    if maya_window_util is not None:
        return shiboken.wrapInstance(long(maya_window_util), QtWidgets.QMainWindow)


def loadUi(uiFile):
    ''' Parses an UI file '''
    parsed = xml.parse(uiFile)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text

    with open(uiFile, 'r') as f:
        o = StringIO()
        frame = {}

        pyside2uic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame

        # Fetch the base_class and form class based on their type in the xml from designer
        form_class = frame['Ui_%s' % form_class]
        base_class = eval('%s' % widget_class)
        return form_class, base_class
