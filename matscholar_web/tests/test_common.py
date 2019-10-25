import unittest

import dash_html_components as html

from matscholar_web.view import core_view_html, footer_html, nav_html

"""
Tests for the core dash view.
"""


class TestCoreView(unittest.TestCase):
    def test_core_views(self):
        self.assertTrue(isinstance(core_view_html(), html.Div))
        self.assertTrue(isinstance(footer_html(), html.Div))
        self.assertTrue(isinstance(nav_html(), html.Div))
