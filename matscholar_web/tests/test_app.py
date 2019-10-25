from matscholar_web.tests.util import MatScholarWebBaseTest
from matscholar_web.app import display_app_html

"""
Tests for callbacks in the main app which are not tested elsewhere.
"""

# Functions to exclude from this test
EXCLUDE = ["guided_search_box_elastic_html"]


class TestCoreAppCallbacks(MatScholarWebBaseTest):
    def test_display_app(self):
        f = display_app_html
        arg_combos = [(a, ) for a in ["/", "/search", "/about", "/extract", "/journals"]]
        self.run_test_for_individual_arg_combos(f, arg_combos)
