import json
import os
import unittest

import matscholar_web
from matscholar_web.util import load_static_data_file


"""
Tests for core utilities.
"""


class TestCoreUtils(unittest.TestCase):
    def setUp(self) -> None:
        rootdir = os.path.dirname(os.path.abspath(matscholar_web.__file__))
        data_dir = os.path.join(rootdir, "assets/data/")
        self.test_fname = "test_file.json"
        self.test_fpath = os.path.join(data_dir, self.test_fname)
        self.true_data = {"a": [1, 2, 3], "b": "something"}

    def test_load_static_file(self):
        with open(self.test_fpath, "w") as f:
            json.dump(self.true_data, f)
        loaded_data = load_static_data_file(self.test_fname)
        self.assertEqual(self.true_data, loaded_data)

    def tearDown(self) -> None:
        os.remove(self.test_fpath)
