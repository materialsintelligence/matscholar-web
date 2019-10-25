from matscholar_web.tests.util import MatScholarWebBaseTest
import matscholar_web.about.view as msweb_aview

"""
Tests for the about app view.
"""

# Functions to exclude from this test
EXCLUDE = []


class TestAboutViews(MatScholarWebBaseTest):
    def test_search_view(self):
        self.run_test_for_all_functions_in_module(msweb_aview, EXCLUDE)
