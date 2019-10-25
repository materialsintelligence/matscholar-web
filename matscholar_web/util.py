import json
import os


"""
Utils for all apps.
"""


def load_static_data_file(fname):
    """
    Load a static json file from the filename in the /assets/data folder.

    Args:
        fname (str): The filename in matscholar_web/assets/data.

    Returns:
        (dict): The file loaded from json.
    """
    _topdir = os.path.abspath(os.path.dirname(__file__))
    _target = os.path.abspath(os.path.join(_topdir, f"assets/data/{fname}"))
    with open(_target, "r") as f:
        file_as_dict = json.load(f)
    return file_as_dict
