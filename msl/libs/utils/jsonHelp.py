# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------
#
# Methods that handles commons json operations.
#
# v1 - 12/2017
# v2 - 03/2018 - Fix invalid json files
# v3 - 10/2018 - Moved from class to direct import methods
# --------------------------------------------------------------------------------------------
import json
import os


def getSimpleJson(jsonFile, queryValue):
    ''' Reads a variable from json file
    jsonFile :: system file to read data.
    queryValue :: value from dictionary to query value
    '''
    if not os.path.exists(jsonFile):
        print("getSimpleJson: Config File not found: {} for Value {}.".format(
            jsonFile, queryValue))
        return False

    with open(jsonFile, 'r') as fIn:
        try:
            jsonContainer = json.load(fIn)
        except ValueError as e:
            print("JSON object issue: {}".format(str(e)))
            return False
    return jsonContainer.get(queryValue)


def getDictJson(jsonFile):
    ''' Reads a dict from json file
    jsonFile :: system file to read data.
    '''
    if not os.path.exists(jsonFile):
        print("getDictJson: Config File not found: {}.".format(jsonFile))
        return False

    with open(jsonFile, 'r') as fIn:
        try:
            return json.load(fIn)
        except ValueError as e:
            print("JSON object issue: {}".format(str(e)))
            return False


def saveDictJson(dataDict, jsonFile):
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


def updateDictJson(values, jsonFile):
    ''' Opens a json file, load its params,
    add new keys and save it
    '''
    if not os.path.exists(jsonFile):
        dictData = {}
        with open(jsonFile, 'w') as loadedJsn:
            json.dump(dictData, loadedJsn, sort_keys=True, indent=4)

    # opens and read json into dictData
    with open(jsonFile, 'r') as loadedJsn:
        dictData = json.load(loadedJsn)
        dictData.update(values)

    with open(jsonFile, 'w') as loadedJsn:
        json.dump(dictData, loadedJsn, sort_keys=True, indent=4)
