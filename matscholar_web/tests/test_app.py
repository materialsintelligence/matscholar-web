import dash_html_components as html

from matscholar_web.app import display_app_html
from matscholar_web.tests.util import MatScholarWebBaseTest, VALID_PAGES


"""
Tests for callbacks in the main app which are not tested elsewhere.
"""


class TestCoreAppCallbacks(MatScholarWebBaseTest):
    def test_display_app(self):
        f = display_app_html
        arg_combos = [(a,) for a in VALID_PAGES]
        valid_types = (str, dict, html.Div)
        for arg_combo in arg_combos:
            o = f(*arg_combo)
            self.assertTrue(isinstance(o, valid_types))
