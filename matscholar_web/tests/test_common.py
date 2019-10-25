import unittest
from inspect import signature

import dash_html_components as html

from matscholar_web.tests.util import get_all_functions_in_module
import matscholar_web.common as common

"""
Tests for the core common dash views.
"""

# Functions to exclude from this test
EXCLUDE = ["common_null_warning_html"]


class TestCoreCommonViews(unittest.TestCase):
    def test_core_common_views(self):
        functions = get_all_functions_in_module(common)
        for fname, f in functions.items():
            if fname in EXCLUDE:
                print(f"Skipping {fname}")
                continue
            else:
                print(f"Testing: {fname}")
                params = signature(f).parameters
                n_args = len(params)
                if n_args == 0: # this function takes no args
                    o = f()
                    if "_html" in fname:
                        self.assertTrue(isinstance(o, html.Div))
                    else:
                        self.assertFalse(isinstance(o, html.Div))
                else:
                    fake_args = ["arg"] * n_args
                    o = f(*fake_args)
                    if "_html" in fname:
                        self.assertTrue(isinstance(o, html.Div))
                    else:
                        self.assertFalse(isinstance(o, html.Div))
