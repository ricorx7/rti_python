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

    # The path to this JSON file will not work if run from python script
    # But if built as an application with pyinstaller, this path will work
    json_file_path = os.path.join(script_dir, 'ADCP/AdcpCommands.json')
    try:
        cmds = json.loads(open(json_file_path).read())
        return cmds
    except Exception as e:
        print("Error opening predictor.JSON file at: " + json_file_path, e)
        try:
            script_dir = ""
            json_file_path = os.path.join(script_dir, 'ADCP/AdcpCommands.json')
            cmds = json.loads(open(json_file_path).read())
            return cmds
        except Exception as e1:
            print("Error opening predictor.JSON file at: " + json_file_path, e1)

    return None