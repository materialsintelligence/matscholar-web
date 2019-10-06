import os
import json

# Stats data, shared among all apps and views
def load_static_data_file(fname):
    _topdir = os.path.abspath(os.path.dirname(__file__))
    _target = os.path.abspath(
        os.path.join(_topdir, f"assets/data/{fname}")
    )
    with open(_target, "r") as f:
        stats = json.load(f)
    return stats