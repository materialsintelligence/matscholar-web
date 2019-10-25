import matscholar_web.view as msweb_view
from matscholar_web.tests.util import MatScholarWebBaseTest

"""
Tests for the core dash view.
"""

# Functions to exclude from this test
EXCLUDE = []


class TestCoreView(MatScholarWebBaseTest):
    def test_core_views(self):
        self.run_test_for_all_functions_in_module(msweb_view, EXCLUDE)
