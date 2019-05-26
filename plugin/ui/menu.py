# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------
# Builds maya arcane menu based on config file.
# --------------------------------------------------------------------------------------------

import maya.cmds as cmds
import maya.mel as mel
import os
import ConfigParser
from ConfigParser import NoOptionError
menuConfigFile = os.path.join(os.path.dirname(__file__), 'menuConfig.ini')


class menuCreator():
    def __init__(self):
        ''' creates maya menu based on config file '''
        self.parser = ConfigParser.ConfigParser()
        self.parser.read(menuConfigFile)
        self.menuMainTitle = self.parser.get('General', 'label')

        global ArcaneTools_MainMenu
        self.gMainWindow = mel.eval("$temp= $gMainWindow")
        ArcaneTools_MainMenu = 'ccArcaneToolsMenu'
        self.createHeader()
        self.parseMenu()

    def createHeader(self):
        ''' creates main menu '''
        # Deletes menu if exist
        if(cmds.menu(ArcaneTools_MainMenu, q=True, exists=True)):
            cmds.deleteUI(ArcaneTools_MainMenu, menu=True)

        cmds.setParent(self.gMainWindow)
        cmds.menu(ArcaneTools_MainMenu, label=self.menuMainTitle.upper(), p=self.gMainWindow, to=True)

    def parseMenu(self):
        ''' parses ini file and creates menuitems '''
        for app in self.parser.sections():
            menuType = self.parser.get(app, 'type')
            label = self.parser.get(app, 'label')
            command = self.parser.get(app, 'command')
            tree = self.parser.get(app, 'tree')
            try:
                icon = self.parser.get(app, 'icon')
            except NoOptionError:
                icon = ''
            if menuType == 'script':
                if tree == 'root':
                    cmds.setParent(ArcaneTools_MainMenu, menu=True)
                self.createMenuItem(app, label, command, icon)
            elif menuType == 'subMenu':
                cmds.setParent(ArcaneTools_MainMenu, menu=True)
                self.createSubMenuGroup(label)

    def createSubMenuGroup(self, label):
        ''' creates a submenu '''
        cmds.menuItem(label=label, sm=True, to=True)

    def createMenuItem(self, app, label, command, icon):
        ''' creates item menu '''
        cmds.menuItem(label=label, stp="python", c=command, image=icon)

    @staticmethod
    def unloadMenu():
        ''' unload menu from maya '''
        import maya.cmds as cmds
        cmds.deleteUI(ArcaneTools_MainMenu, menu=True)
