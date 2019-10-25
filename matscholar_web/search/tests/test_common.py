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
        fname = "results_label_html"
        for arg in ["entities", "materials", "abstracts"]:
            print(f"Test: {arg} in {fname}")
            o = msweb_scommon.results_label_html(arg)
            self._basic_type_check_on_function(fname, o)

    def test_big_label_and_disclaimer_html(self):
        fname = "big_label_and_disclaimer_html"
        for arg in ["entities", "materials", "abstracts"]:
            print(f"Test: {arg} in {fname}")
            o = msweb_scommon.big_label_and_disclaimer_html(arg)
            self._basic_type_check_on_function(fname, o)
