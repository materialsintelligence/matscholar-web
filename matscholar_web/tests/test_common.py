from matscholar_web.tests.util import MatScholarWebBaseTest

import matscholar_web.common as common

"""
Tests for the core common dash views.
"""

# Functions to exclude from this test
EXCLUDE = ["common_null_warning_html"]


class TestCoreCommonViews(MatScholarWebBaseTest):
    def test_core_common_views(self):
        self.run_test_for_all_functions_in_module(common, EXCLUDE)
