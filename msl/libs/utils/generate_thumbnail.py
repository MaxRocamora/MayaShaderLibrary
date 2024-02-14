# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# Opens a maya standalone instance and do a thumbnail render for given shader.
# ----------------------------------------------------------------------------------------
import maya.cmds as cmds
import maya.standalone as std
import sys
import os

print('Loading Maya StandAlone...')

std.initialize(name='python')

print('Generating Thumbnail...')

shaderRig = sys.argv[1]
shaderFile = sys.argv[2]
rndFile = os.path.splitext(sys.argv[3])[0]


def setup_render_file():
    """Open shader lighting file and import shader file."""
    cmds.file(shaderRig, force=True, open=True)
    cmds.file(
        shaderFile,
        i=True,
        type='mayaAscii',
        ignoreVersion=True,
        ns='shd',
        options='v=0;',
        pr=True,
    )


def set_shader_ball():
    """Set shader ball for rendering."""
    shader = 'shd:shdBallShape'
    shaderSGConn = cmds.listConnections(shader, d=True, et=True, t='shadingEngine')
    sg = shaderSGConn[0]
    for geo in cmds.ls('*_GEO'):
        cmds.sets(geo, edit=True, forceElement=sg)
    cmds.hide(shader)


def render_thumbnail():
    """Render thumbnail for the shader."""

    from mtoa.cmds.arnoldRender import arnoldRender

    cmds.loadPlugin('mtoa')
    cmds.setAttr('defaultArnoldDriver.ai_translator', 'png', type='string')
    cmds.setAttr('defaultArnoldDriver.pre', rndFile, type='string')
    arnoldRender(200, 200, True, True, 'RND_Camera', ' -layer defaultRenderLayer')


setup_render_file()
set_shader_ball()
render_thumbnail()

print('Done')
