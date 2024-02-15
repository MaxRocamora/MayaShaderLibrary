# ----------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
# https://github.com/MaxRocamora/MayaShaderLibrary
#
# Methods that handles load/save json to file.
# ----------------------------------------------------------------------------------------
import json
import os

from msl.libs.logger import log


def load_json(json_file: str):
    """Reads a dict from json file."""
    if not os.path.exists(json_file):
        log.warning(f'load_json: JSON File not found: {json_file}.')
        return False

    with open(json_file) as fIn:
        try:
            return json.load(fIn)
        except ValueError as e:
            log.warning(f'JSON object issue: {str(e)}')
            return False


def save_json(data: dict, json_file: str):
    """Saves a dictionary into a json file.

    Args:
        data (dict) : info dictionary to save
        json_file (filepath) : target file to save into
    """
    if os is None:
        return

    if not os.path.dirname(json_file):
        os.mkdir(json_file)

    try:
        with open(json_file, 'w') as loadedJsn:
            json.dump(data, loadedJsn, sort_keys=True, indent=4)
    except OSError:
        log.warning('IOError: No such file of directory:', json_file)
