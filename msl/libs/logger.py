# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# Stream Logger
# ----------------------------------------------------------------------------------------
import logging

log = logging.getLogger('ShaderLibrary')
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('ShaderLibrary - %(levelname)-7s | %(message)s')
stream_handler.setFormatter(formatter)
log.propagate = False
log.setLevel(logging.DEBUG)
if len(log.handlers) == 0:
    log.addHandler(stream_handler)


if __name__ == '__main__':
    log.info('test info')
    log.warning('test warning')
    log.error('test error')
    log.critical('test critical')
    log.debug('test debug')
