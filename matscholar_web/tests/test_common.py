import unittest

import dash_html_components as html

from matscholar_web.tests.util import get_all_functions_in_module
import matscholar_web.common as common

"""
Tests for the core common dash views.
"""


class TestCoreCommonViews(unittest.TestCase):
    def test_core_common_views(self):
        functions = get_all_functions_in_module(common)
        for fname, f in functions.items():
            print(f"Testing: {fname}")
            if "_html" in

