from matscholar_web.tests.util import MatScholarWebBaseTest

import matscholar_web.search.common as msweb_scommon

"""
Tests for the search common views.
"""

# Functions to exclude from this test
EXCLUDE = ["results_label_html", "big_label_and_disclaimer_html"]


class TestSearchCommonViews(MatScholarWebBaseTest):
    def test_common_views(self):
        self.run_test_for_all_functions_in_module(msweb_scommon, EXCLUDE)

    def test_results_label_html(self):
        f = msweb_scommon.results_label_html
        arg_combos = [(a, ) for a in ["entities", "materials", "abstracts"]]
        self.run_test_for_individual_arg_combos(f, arg_combos)

    def test_big_label_and_disclaimer_html(self):
        f = msweb_scommon.big_label_and_disclaimer_html
        arg_combos = [(a, ) for a in ["entities", "materials", "abstracts"]]
        self.run_test_for_individual_arg_combos(f, arg_combos)
