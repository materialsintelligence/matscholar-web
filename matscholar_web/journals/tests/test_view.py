from matscholar_web.tests.util import MatScholarWebBaseTest

import matscholar_web.journals.view as msweb_jv

"""
Tests for the journals view.
"""

# Functions to exclude from this test
EXCLUDE = []


class TestJournalsView(MatScholarWebBaseTest):
    def test_journal_views(self):
        self.run_test_for_all_functions_in_module(msweb_jv, EXCLUDE)