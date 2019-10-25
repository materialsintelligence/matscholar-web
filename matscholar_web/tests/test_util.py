import os
import json
import unittest

import matscholar_web
from matscholar_web.util import load_static_data_file


"""
Tests for core utilities.
"""


class TestCoreUtils(unittest.TestCase):
    def test_load_static_file(self):
        rootdir = os.path.dirname(os.path.abspath(matscholar_web.__file__))
        data_dir = os.path.join(rootdir, "assets/data/")
        test_fname = "test_file.json"
        test_fpath = os.path.join(data_dir, test_fname)
        true_data = {"a": [1,2,3], "b": "something"}
        with open(test_fpath, "w") as f:
            json.dump(true_data, f)
        loaded_data = load_static_data_file(test_fname)
        self.assertEqual(true_data, loaded_data)