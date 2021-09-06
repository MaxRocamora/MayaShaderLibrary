'''
Opens a maya standalone instance and do a thumbnail render for given shader.
'''
from __future__ import print_function
import sys
import os

print('Loading Maya StandAlone...')

import maya.standalone as std
std.initialize(name='python')

print('Generating Thumbnail...')

import maya.cmds as cmds

shaderRig = sys.argv[1]
shaderFile = sys.argv[2]
rndFile = os.path.splitext(sys.argv[3])[0]


def setupRenderFile():
    cmds.file(shaderRig, force=True, open=True)
    cmds.file(shaderFile, i=True, type="mayaAscii", ignoreVersion=True,
              ns="shd", options="v=0;", pr=True)


def setShaderBall():
    shader = 'shd:shdBallShape'
    shaderSGConn = cmds.listConnections(shader, d=True, et=True, t='shadingEngine')
    sg = shaderSGConn[0]
    for geo in cmds.ls('*_GEO'):
        cmds.sets(geo, edit=True, forceElement=sg)
    cmds.hide(shader)


def renderThumbnail():
    # arnold render
    from mtoa.cmds.arnoldRender import arnoldRender
    cmds.loadPlugin('mtoa')
    cmds.setAttr("defaultArnoldDriver.ai_translator", "png", type="string")
    cmds.setAttr("defaultArnoldDriver.pre", rndFile, type="string")
    arnoldRender(200, 200, True, True, 'RND_Camera', ' -layer defaultRenderLayer')


setupRenderFile()
setShaderBall()
renderThumbnail()

print('Done')
