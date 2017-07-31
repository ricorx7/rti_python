import os
import json


def get_json():
    """
    Get the JSON file.  There are 2 locations based off local testing or a deployed
    application.  This will check the first location which is the directory the application
    is running.  The second location is the root directory.
    :return:
    """
    # Get the descriptions from the json file
    # script_dir = ""
    script_dir = os.path.dirname(__file__)

    json_file = "AdcpCommands.json"

    # Create a file name with folder path
    json_file_adcp = os.path.join("ADCP", json_file)

    # The path to this JSON file will not work if run from python script
    # But if built as an application with pyinstaller, this path will work
    json_file_path = os.path.join(script_dir, json_file_adcp)
    cmds = _get_json(json_file_path)

    # If JSON not found, try another path
    if cmds is None:
        # Try local file path
        script_dir = ""
        json_file_path = os.path.join(script_dir, json_file_adcp)
        cmds = _get_json(json_file_path)

        # If JSON not found, try another path
        if cmds is None:
            #script_back = os.path.join()
            json_file_path = os.getcwd() + os.sep + ".." + os.sep + ".." + os.sep + ".." + os.sep + "ADCP" + os.sep + json_file
            #json_file_path = os.path.join(script_back, json_file_adcp)
            cmds = _get_json(json_file_path)

    return cmds


def _get_json(json_file_path):
    # The path to this JSON file will not work if run from python script
    # But if built as an application with pyinstaller, this path will work

    try:
        cmds = json.loads(open(json_file_path).read())
        return cmds
    except Exception as e1:
        print("Error opening AdcpCommands.JSON file at: " + json_file_path, e1)
        return None

