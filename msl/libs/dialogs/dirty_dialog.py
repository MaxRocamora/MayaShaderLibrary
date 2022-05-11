import maya.cmds as cmds

from msl.libs.logger import log


def dirty_file_dialog():
    ''' Ask user to save their current scene
    if it was modified since last save.
    '''
    if not cmds.file(query=True, modified=True):
        return

    msg = 'Current file is modified. Do you want to save this file?'
    result = cmds.confirmDialog(title='Save changes',
                                message=msg,
                                button=['yes', 'no'],
                                defaultButton='yes',
                                cancelButton='no',
                                dismissString='no')
    if result == 'yes':
        try:
            cmds.file(save=True, type='mayaAscii')
        except RuntimeError as e:
            log.error(e)
