# --------------------------------------------------------------------------------------------
# Maya Shader Library
# Author: maxirocamora@gmail.com
#
# Methods that handles commons json operations.
# --------------------------------------------------------------------------------------------
import json
import os


def load_json(jsonFile):
    ''' Reads a dict from json file
    jsonFile :: system file to read data.
    '''
    if not os.path.exists(jsonFile):
        print("load_json: JSON File not found: {}.".format(jsonFile))
        return False

    with open(jsonFile, 'r') as fIn:
        try:
            return json.load(fIn)
        except ValueError as e:
            print("JSON object issue: {}".format(str(e)))
            return False


def save_json(dataDict, jsonFile):
    ''' Saves a dictionary into a json file
    Args:
        dataDict (dictionary) : info dictionary to save
        jsonFile (file) : target file to save into
    '''
    if os is None:
        return

    if not os.path.dirname(jsonFile):
        os.mkdir(jsonFile)

    try:
        with open(jsonFile, 'w') as loadedJsn:
            json.dump(dataDict, loadedJsn, sort_keys=True, indent=4)
    except IOError:
        print('IOError: No such file of directory:', jsonFile)
